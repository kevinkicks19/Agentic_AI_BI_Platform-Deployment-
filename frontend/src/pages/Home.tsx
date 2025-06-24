import React from 'react';
import Chat from '../components/Chat';
import FileUpload from '../components/FileUpload';
import PersonaSelector from '../components/PersonaSelector';

const Home: React.FC = () => {
  return (
    <>
      <h1>Welcome to the Home Page</h1>
      <PersonaSelector />
      <Chat />
      <FileUpload />
    </>
  );
};

export default Home; 