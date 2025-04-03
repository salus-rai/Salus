const fs = require('fs');
const path = require('path');

// Directory to start from (set to the src folder for an Angular app)
const directoryPath = path.join(__dirname, 'src');

// New license comment to replace the old ones
const newLicenseComment = `<!-- 
# SPDX-License-Identifier: MIT
# Copyright 2024 - 2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-->`;

function updateLicenseInFiles(dirPath) {
    fs.readdirSync(dirPath).forEach(file => {
        const fullPath = path.join(dirPath, file);

        if (fs.statSync(fullPath).isDirectory()) {
            // Recursively go through subdirectories
            updateLicenseInFiles(fullPath);
        } else if (fullPath.endsWith('.html')) {
            // Only process specific file types
            const fileContent = fs.readFileSync(fullPath, 'utf-8');

            // Replace the old license comment with the new one
            const updatedContent = fileContent.replace(
                /\/\*\*?[\s\S]*?SPDX-License-Identifier: MIT[\s\S]*?\*\/|<!--[\s\S]*?MIT license[\s\S]*?-->/g,
                newLicenseComment
            );

            // Write the updated content back to the file
            fs.writeFileSync(fullPath, updatedContent);
            console.log(`Updated license in: ${fullPath}`);
        }
    });
}

// Start the process
updateLicenseInFiles(directoryPath);