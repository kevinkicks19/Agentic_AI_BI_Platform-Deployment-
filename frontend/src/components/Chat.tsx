import React, { useEffect, useRef, useState } from 'react';
import { chatWithN8nAgent } from '../services/api';
import './Chat.css';

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

interface ChatProps {
  onHandoffStart: (handoffData: any) => void;
  agentType: string;
  sessionId: string;
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

const Chat: React.FC<ChatProps> = ({ onHandoffStart, agentType, sessionId }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);
  
  const handleSendMessage = async (messageContent: string) => {
    const userMessage: Message = { id: Date.now(), role: 'user', content: messageContent };
    setMessages(prev => [...prev, userMessage]);
    setIsTyping(true);

    try {
      let reply = '';
      if (agentType === 'n8n') {
        const response = await chatWithN8nAgent(sessionId, messageContent);
        reply = response.reply;
      } else {
        const response = await fetch(`${API_BASE_URL}/chat`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: messageContent }),
        });
        const data = await response.json();

        // Check if the backend is signaling a handoff to a workflow agent
        if (data.handoff) {
          // Add a system message to inform the user about the switch
          const handoffMessage: Message = {
            id: Date.now() + 1,
            role: 'system',
            content: `Connecting you to ${data.handoff.name}...`,
          };
          setMessages(prev => [...prev, handoffMessage]);

          // Trigger the handoff in the parent component
          setTimeout(() => {
            onHandoffStart(data.handoff);
          }, 1500); // Wait a moment so the user can read the message
        } else {
          // This is a regular response from the coordinator
          const assistantMessage: Message = {
            id: Date.now() + 1,
            role: 'assistant',
            content: data.message,
            buttons: data.buttons,
          };
          setMessages(prev => [...prev, assistantMessage]);
        }
      }
      if (reply) {
        setMessages(prev => [...prev, { id: Date.now() + 1, role: 'assistant', content: reply }]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        id: Date.now() + 1,
        role: 'system',
        content: 'Sorry, there was an error connecting to the server.',
      };
      setMessages(prev => [...prev, errorMessage]);
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
    if ((button as any).action === 'open_n8n_chat') {
      // Trigger the handoff in the parent component
      onHandoffStart({ name: 'n8n Agent', sessionId: null }); // You can pass more context if needed
    } else {
      handleSendMessage(button.value);
    }
  };


  return (
    <div className="chat-container">
      <div className="chat-header">
        <h2>Coordinator Agent</h2>
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
          placeholder="Chat with the coordinator..."
          autoFocus
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
};

export default Chat; 