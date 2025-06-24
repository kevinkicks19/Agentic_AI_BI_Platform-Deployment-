import { useState } from 'react';
import './App.css';
import Chat from './components/Chat';
import NavBar from './components/NavBar';
import Sidebar from './components/Sidebar';
import WorkflowChat from './components/WorkflowChat';

function App() {
  const [activeHandoff, setActiveHandoff] = useState<any>(null);

  const handleHandoffStart = (handoffData: any) => {
    console.log('Handoff started:', handoffData);
    setActiveHandoff(handoffData);
  };

  const handleHandoffEnd = () => {
    console.log('Handoff ended');
    setActiveHandoff(null);
  };

  return (
    <div className="App">
      <NavBar />
      <Sidebar />
      <div className="main-content">
        <header className="App-header">
          <h1>Agentic AI BI Platform</h1>
        </header>
        <main>
          {!activeHandoff ? (
            <Chat onHandoffStart={handleHandoffStart} />
          ) : (
            <WorkflowChat handoffData={activeHandoff} onHandoffEnd={handleHandoffEnd} />
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
