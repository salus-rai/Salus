/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/
const ModuleFederationPlugin = require("webpack/lib/container/ModuleFederationPlugin");
const mf = require("@angular-architects/module-federation/webpack");
const path = require("path");
const share = mf.share;

const sharedMappings = new mf.SharedMappings();
sharedMappings.register(
    path.join(__dirname, 'tsconfig.json'), [ /* mapped paths to share */ ]);

module.exports = {
    output: {
        uniqueName: "rAIFrontend",
        publicPath: "auto"
    },
    optimization: {
        runtimeChunk: false
    },
    resolve: {
        alias: {
            ...sharedMappings.getAliases(),
        }
    },
    experiments: {
        outputModule: true
    },
    plugins: [
        new ModuleFederationPlugin({
            library: { type: "module" },

            // For remotes (please adjust)
            name: "rAIFrontend",
            filename: "remoteEntry.js",
            exposes: {
                './RemoteMfeModule': './src/app/remote-mfe/remote-mfe.module.ts',
            },

            // For hosts (please adjust)
            // remotes: {
            //     "mfe1": "http://localhost:3000/remoteEntry.js",

            // },

            shared: share({
                "@angular/core": { singleton: true, strictVersion: false, requiredVersion: 'auto' },
                "@angular/common": { singleton: true, strictVersion: false, requiredVersion: 'auto' },
                "@angular/common/http": { singleton: true, strictVersion: false, requiredVersion: 'auto' },
                "@angular/router": { singleton: true, strictVersion: false, requiredVersion: 'auto' },

                ...sharedMappings.getDescriptors()
            })

        }),
        sharedMappings.getPlugin()
    ],
};