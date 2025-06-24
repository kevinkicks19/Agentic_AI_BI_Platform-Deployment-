import Alert from '@mui/material/Alert';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import React, { useRef, useState } from 'react';
import { uploadFile } from '../services/api';

const ACCEPTED_TYPES = [
  'text/csv',
  'application/pdf',
  'text/plain',
];

const ACCEPTED_EXTENSIONS = ['.csv', '.pdf', '.txt'];

type FileStatus = 'pending' | 'uploading' | 'success' | 'error';

interface UploadingFile {
  file: File;
  status: FileStatus;
  error?: string;
}

const FileUpload: React.FC = () => {
  const [files, setFiles] = useState<UploadingFile[]>([]);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement | null>(null);

  const handleFiles = (fileList: FileList | null) => {
    if (!fileList) return;
    const newFiles: UploadingFile[] = [];
    for (let i = 0; i < fileList.length; i++) {
      const file = fileList[i];
      const ext = file.name.slice(file.name.lastIndexOf('.')).toLowerCase();
      if (!ACCEPTED_TYPES.includes(file.type) && !ACCEPTED_EXTENSIONS.includes(ext)) {
        setError(`File type not supported: ${file.name}`);
        continue;
      }
      newFiles.push({ file, status: 'pending' });
    }
    if (newFiles.length > 0) {
      setFiles((prev) => [...prev, ...newFiles]);
      setError(null);
      newFiles.forEach((f, idx) => uploadAndTrackFile(f, files.length + idx));
    }
  };

  const uploadAndTrackFile = async (uploadingFile: UploadingFile, index: number) => {
    setFiles((prev) => {
      const updated = [...prev];
      updated[index] = { ...uploadingFile, status: 'uploading' };
      return updated;
    });
    try {
      await uploadFile(uploadingFile.file);
      setFiles((prev) => {
        const updated = [...prev];
        updated[index] = { ...uploadingFile, status: 'success' };
        return updated;
      });
    } catch (err) {
      setFiles((prev) => {
        const updated = [...prev];
        updated[index] = { ...uploadingFile, status: 'error', error: 'Upload failed' };
        return updated;
      });
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    handleFiles(e.dataTransfer.files);
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    handleFiles(e.target.files);
    if (inputRef.current) inputRef.current.value = '';
  };

  const handleRemove = (index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
  };

  return (
    <Box sx={{ maxWidth: 500, mx: 'auto', my: 4 }}>
      <Typography variant="h6" gutterBottom>
        Upload Files (CSV, PDF, TXT)
      </Typography>
      <Paper
        elevation={2}
        sx={{
          p: 3,
          mb: 2,
          border: '2px dashed',
          borderColor: 'primary.main',
          textAlign: 'center',
          bgcolor: 'grey.50',
          cursor: 'pointer',
        }}
        onDrop={handleDrop}
        onDragOver={(e) => e.preventDefault()}
        onClick={() => inputRef.current?.click()}
        aria-label="File drop area"
      >
        <Typography variant="body1" color="textSecondary">
          Drag and drop files here, or click to select files
        </Typography>
        <input
          ref={inputRef}
          type="file"
          multiple
          accept={ACCEPTED_EXTENSIONS.join(',')}
          style={{ display: 'none' }}
          onChange={handleFileInput}
        />
      </Paper>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {files.length > 0 && (
        <List>
          {files.map((f, idx) => (
            <ListItem
              key={f.file.name + f.file.size + idx}
              secondaryAction={
                <Button color="error" size="small" onClick={() => handleRemove(idx)}>
                  Remove
                </Button>
              }
            >
              <ListItemText
                primary={f.file.name}
                secondary={
                  f.status === 'uploading'
                    ? 'Uploading...'
                    : f.status === 'success'
                    ? 'Uploaded'
                    : f.status === 'error'
                    ? f.error || 'Error'
                    : `${(f.file.size / 1024).toFixed(1)} KB`
                }
              />
            </ListItem>
          ))}
        </List>
      )}
    </Box>
  );
};

export default FileUpload; 