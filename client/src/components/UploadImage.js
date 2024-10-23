import React from 'react';
import { useDropzone } from 'react-dropzone';

const UploadImage = ({ onImageUpload }) => {
  const { getRootProps, getInputProps } = useDropzone({
    accept: 'image/*',
    onDrop: acceptedFiles => {
      onImageUpload(acceptedFiles[0]);
    }
  });

  return (
    <div {...getRootProps()} className="upload-image">
      <input {...getInputProps()} />
      <p>Drag 'n' drop an image here, or click to select an image</p>
    </div>
  );
};

export default UploadImage;
