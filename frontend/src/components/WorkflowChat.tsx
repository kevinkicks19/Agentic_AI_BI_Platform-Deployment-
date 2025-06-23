import React, { useEffect, useRef, useState } from 'react';
import './Chat.css'; // We can reuse the same CSS for a consistent look

interface Button {
  label: string;
  value: string;
}

interface Message {
  id: number;
  role: 'user' | 'assistant' | 'system';
  content: string;
  buttons?: Button[];
}

interface WorkflowChatProps {
  handoffData: {
    name: string;
    sessionId: string;
  };
  onHandoffEnd: () => void;
}

const WorkflowChat: React.FC<WorkflowChatProps> = ({ handoffData, onHandoffEnd }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    // Add an initial system message to welcome the user to the new agent chat
    setMessages([
      {
        id: Date.now(),
        role: 'system',
        content: `You are now connected to ${handoffData.name}.`,
      },
    ]);
  }, [handoffData]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (messageContent: string) => {
    const userMessage: Message = { id: Date.now(), role: 'user', content: messageContent };
    setMessages(prev => [...prev, userMessage]);
    setIsTyping(true);

    try {
      // Send directly to n8n webhook with sessionId and message
      const response = await fetch('https://bmccartn.app.n8n.cloud/webhook/ca361862-55b2-49a0-a765-ff06b90e416a/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId: handoffData.sessionId, chatInput: messageContent }),
      });
      const data = await response.json();
      
      const assistantMessage: Message = {
        id: Date.now() + 1,
        role: 'assistant',
        content: data.output || data.message || JSON.stringify(data),
        // Optionally handle buttons if n8n returns them
        buttons: data.buttons,
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error during workflow chat:', error);
      const errorMessage: Message = {
        id: Date.now() + 1,
        role: 'system',
        content: 'An error occurred. Returning to the main coordinator.',
      };
      setMessages(prev => [...prev, errorMessage]);
      setTimeout(() => {
        onHandoffEnd();
      }, 2500);
    } finally {
      setIsTyping(false);
    }
  };

  const handleFormSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim()) {
      handleSendMessage(input);
      setInput('');
    }
  };

  const handleButtonClick = (button: Button) => {
    handleSendMessage(button.value);
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h2>{handoffData.name}</h2>
      </div>
      <div className="messages">
        {messages.map(msg => (
          <div key={msg.id} className={`message ${msg.role}`}>
            <p>{msg.content}</p>
            {msg.buttons && (
              <div className="buttons">
                {msg.buttons.map((btn, index) => (
                  <button key={index} onClick={() => handleButtonClick(btn)}>
                    {btn.label}
                  </button>
                ))}
              </div>
            )}
          </div>
        ))}
        {isTyping && (
          <div className="message assistant">
            <div className="typing-indicator">
              <span></span><span></span><span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <form onSubmit={handleFormSubmit} className="input-form">
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Type your message..."
          autoFocus
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
};

export default WorkflowChat; 