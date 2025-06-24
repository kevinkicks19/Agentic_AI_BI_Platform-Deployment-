import Box from '@mui/material/Box';
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
import Typography from '@mui/material/Typography';
import React, { useState } from 'react';

const PERSONAS = [
  'Consultant',
  'Project Manager',
  'Business Analyst',
  'Solution Architect',
];

const PersonaSelector: React.FC = () => {
  const [persona, setPersona] = useState<string>(PERSONAS[0]);

  const handleChange = (
    _event: React.MouseEvent<HTMLElement>,
    newPersona: string | null
  ) => {
    if (newPersona !== null) {
      setPersona(newPersona);
    }
  };

  return (
    <Box sx={{ my: 4, textAlign: 'center' }}>
      <Typography variant="h6" gutterBottom>
        Select Your Persona
      </Typography>
      <ToggleButtonGroup
        value={persona}
        exclusive
        onChange={handleChange}
        aria-label="persona selector"
        color="primary"
      >
        {PERSONAS.map((p) => (
          <ToggleButton key={p} value={p} aria-label={p}>
            {p}
          </ToggleButton>
        ))}
      </ToggleButtonGroup>
      <Typography variant="body1" sx={{ mt: 2 }}>
        Current Persona: <strong>{persona}</strong>
      </Typography>
    </Box>
  );
};

export default PersonaSelector; 