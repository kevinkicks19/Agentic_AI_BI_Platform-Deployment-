import React, { useState } from 'react';
import { triggerWorkflow } from '../services/api';
import Chat from './Chat';

const WorkflowTestButton: React.FC = () => {
  const [showChat, setShowChat] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);

  const handleTestWorkflow = async () => {
    const response = await triggerWorkflow({ type: 'test' });
    if (response.success) {
      setSessionId(response.sessionId);
      setShowChat(true);
    } else {
      alert('Failed to trigger workflow');
    }
  };

  return (
    <>
      <button onClick={handleTestWorkflow}>Test Workflow</button>
      {showChat && sessionId && (
        <Chat agentType="n8n" sessionId={sessionId} />
      )}
    </>
  );
};

export default WorkflowTestButton; 