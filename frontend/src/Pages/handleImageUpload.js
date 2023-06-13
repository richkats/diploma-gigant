import React, { useState } from 'react';

export const ImageUploader = () => {
    const [preview, setPreview] = useState(null);

    const handleImageUpload = (event) => {
        const file = event.target.files[0];
        const reader = new FileReader();

        reader.onloadend = () => {
            setPreview(reader.result);
        };

        if (file) {
            reader.readAsDataURL(file);
        }
    }
}
