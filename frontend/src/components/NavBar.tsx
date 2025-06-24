import React from 'react';

const navStyle: React.CSSProperties = {
  position: 'fixed',
  top: 0,
  left: 0,
  width: '100%',
  height: '56px',
  background: '#222',
  color: '#fff',
  display: 'flex',
  alignItems: 'center',
  boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
  zIndex: 1100,
};

const sectionStyle: React.CSSProperties = {
  display: 'flex',
  alignItems: 'center',
  height: '100%',
};

const leftStyle: React.CSSProperties = {
  ...sectionStyle,
  flex: 1,
  justifyContent: 'flex-start',
};

const centerStyle: React.CSSProperties = {
  ...sectionStyle,
  flex: 1,
  justifyContent: 'center',
};

const rightStyle: React.CSSProperties = {
  ...sectionStyle,
  flex: 1,
  justifyContent: 'flex-end',
};

const buttonStyle: React.CSSProperties = {
  background: 'none',
  border: '1px solid #444',
  color: '#fff',
  borderRadius: '4px',
  padding: '0.5rem 1rem',
  cursor: 'pointer',
  fontSize: '1rem',
  margin: '0 0.5rem',
};

const NavBar: React.FC = () => {
  return (
    <nav style={navStyle} className="navbar">
      <div style={leftStyle}>
        <button style={buttonStyle}>Project Dir</button>
      </div>
      <div style={centerStyle}>
        <button style={buttonStyle}>Docs</button>
      </div>
      <div style={rightStyle}>
        <button style={buttonStyle}>User Info</button>
      </div>
    </nav>
  );
};

export default NavBar; 