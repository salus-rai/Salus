/**
# SPDX-License-Identifier: MIT
# Copyright 2024 - 2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/
const fs = require('fs');
const path = require('path');
const { exec } = require('shelljs');

//const proxyConfigPath = 'proxy.config.json';
const angularPath = 'angular.json';
// const appConstantPath = 'src/app/app.constants.ts';
//const stylePath = 'styles.scss';
const envFilePath = 'src/environments/environment.ts';
const urlListFilePath = 'src/app/urlList.ts';
// const webpackConfigPath = 'webpack.config.js';
//const appmodulePath = 'src/app/app.module.ts';

const URLDATA = {
    HOMEFILEPATHURL: null,
    DICOMFILEPATHURL: null,
    MASTERURL: null,
    ENABLESEARCH: null,
    NG_SERVE_CMD: null,
    AUTHORITY_API: null,
    AUTH_TOKEN: null
};

const readFile = filePath => {
    return new Promise(async(resolve, reject) => {
        fs.readFile(path.normalize(filePath), 'utf8', (err, data) => {
            if (err) {
                console.log(err);
                reject(err);
            }
            resolve(data);
        });
    });
};

const writeFile = (filePath, data) => {
    return new Promise(async(resolve, reject) => {
        fs.writeFile(path.normalize(filePath), data, 'utf8', err => {
            if (err) {
                console.log(err);
                reject(err);
            }
            console.log('Successfully written :: ' + filePath);
            resolve('success');
        });
    });
};

const NgServeProxyConfig = () => {
    if (!URLDATA.NG_SERVE_CMD) {
        console.error('NG_SERVE_CMD is not set in URLDATA');
        return;
    }

    // Sanitize and validate the command
    const sanitizedCommand = sanitizeCommandInput(URLDATA.NG_SERVE_CMD);
    if (!validateCommand(sanitizedCommand)) {
        console.error('Invalid command detected');
        return;
    }

    console.log('Executing ng serve with command:', sanitizedCommand);
    exec(sanitizedCommand, { stdio: 'inherit' }, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing ng serve: ${error.message}`);
            return;
        }
        if (stderr) {
            console.error(`stderr: ${stderr}`);
            return;
        }
        console.log(`stdout: ${stdout}`);
    });
};

const updateEnvFile = async() => {
    return new Promise(async(resolve, reject) => {
        console.log('updating env data');
        const envFileData = await readFile(envFilePath);
        const fileData = envFileData
            .replace(/HOMEFILEPATHURL/g, URLDATA.HOMEFILEPATHURL)
            .replace(/DICOMFILEPATHURL/g, URLDATA.DICOMFILEPATHURL)

        const writeRes = await writeFile(envFilePath, fileData);
        resolve(writeRes);
    });
};

// const updateWebpackConfig = async() => {
//     return new Promise(async(resolve, reject) => {
//         console.log('updating webpack config data');
//         const webpackConfigFileData = await readFile(webpackConfigPath);
//         const webpackConfigFileData2 = webpackConfigFileData.replace(/MFE_URL/g, URLDATA.MFE_URL);

//         const writeRes = await writeFile(webpackConfigPath, webpackConfigFileData2);
//         resolve(writeRes);
//     });
// };

const updateURLlistTs = async() => {
    return new Promise(async(resolve, reject) => {
        console.log('updating urlList.ts data');
        const proxyConfigFileData = await readFile(urlListFilePath);
        let updatedData = proxyConfigFileData
            .replace(/HOMEFILEPATHURL/g, URLDATA.HOMEFILEPATHURL)
            .replace(/DICOMFILEPATHURL/g, URLDATA.DICOMFILEPATHURL)
            .replace(/MASTERURL/g, URLDATA.MASTERURL)
            .replace(/'ENABLESEARCH'/g, URLDATA.ENABLESEARCH)
            .replace(/AUTHORITY_API/g, URLDATA.AUTHORITY_API)
            .replace(/AUTH_TOKEN/g, URLDATA.AUTH_TOKEN);
        const writeRes = await writeFile(urlListFilePath, updatedData);
        resolve(writeRes);
    });
};

const setDataFromENV = () => {
    (URLDATA['HOMEFILEPATHURL'] = process.env['HOMEFILEPATHURL']),
    (URLDATA['DICOMFILEPATHURL'] = process.env['DICOMFILEPATHURL']),
    (URLDATA['MASTERURL'] = process.env['MASTERURL']),
    (URLDATA['ENABLESEARCH'] = process.env['ENABLESEARCH']),
    (URLDATA['AUTHORITY_API'] = process.env['AUTHORITY_API']),
    (URLDATA['NG_SERVE_CMD'] = process.env['NG_SERVE_CMD']),
    (URLDATA['AUTH_TOKEN'] = process.env['AUTH_TOKEN']);

};

const runLocally = async() => {
    (URLDATA['HOMEFILEPATHURL'] = 'http://localhost:30055'),
    (URLDATA['DICOMFILEPATHURL'] = 'http://localhost:30055'),
    (URLDATA['MASTERURL'] = 'http://localhost:30016/api/v1/rai/admin/ConfigApi'),
    (URLDATA['ENABLESEARCH'] = false),
    (URLDATA['AUTHORITY_API'] = 'http://localhost:30019/v1/rai/backend/pageauthoritynew'),
    (URLDATA['NG_SERVE_CMD'] = 'ng serve --host 0.0.0.0 --port 30055 --disable-host-check'),
    (URLDATA['AUTH_TOKEN'] = '<YOUR_AUTH_TOKEN>');
};

const runApplication = async function() {
    setDataFromENV();
    // await runLocally();

    //const proxyConfigRes = await updateProxyConfig();
    //const webpackConfigRes = await updateWebpackConfig();
    const URLlistTsRes = await updateURLlistTs();
    const EnvFile = await updateEnvFile();
    //const AngularFile = await updateAngular();
    // const StyleFile = await updateStyle();
    //const AppConstantFile = await updateAppConstant();
    //const AppModuleConstantFile = await updateAppModuleConstant();
    NgServeProxyConfig();
};
const sanitizeCommandInput = (input) => {
    console.log("sanitize")
        // This allows alphanumeric characters, spaces, hyphens, and equals signs
    const sanitized = input.replace(/[^a-zA-Z0-9\s\-=\.:/]/g, '');
    return sanitized;
};

const validateCommand = (command) => {
    console.log("validate")
        // Check if the command starts with 'ng' and contains only safe arguments
    return /^ng\s/.test(command); // 'ng' followed by any valid arguments
};
runApplication();