import React from 'react';
import { Link } from 'react-router-dom';

const sidebarStyle: React.CSSProperties = {
  position: 'fixed',
  top: 0,
  left: 0,
  width: '200px',
  height: '100vh',
  background: '#222',
  color: '#fff',
  display: 'flex',
  flexDirection: 'column',
  padding: '2rem 1rem',
  gap: '1.5rem',
  boxShadow: '2px 0 8px rgba(0,0,0,0.08)',
  zIndex: 1000,
};

const linkStyle: React.CSSProperties = {
  color: '#fff',
  textDecoration: 'none',
  fontWeight: 'bold',
  fontSize: '1.1rem',
};

const Sidebar: React.FC = () => {
  return (
    <aside style={sidebarStyle} className="sidebar">
      <Link to="/" style={linkStyle}>Overview</Link>
      <a href="#" style={linkStyle}>Project Dir (Files)</a>
      <a href="#" style={linkStyle}>Workflow Visualization</a>
      <a href="#" style={linkStyle}>Settings</a>
    </aside>
  );
};

export default Sidebar; 