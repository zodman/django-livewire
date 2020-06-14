import md5 from 'md5'
import fs from 'fs-extra'
import babel from 'rollup-plugin-babel';
import alias from '@rollup/plugin-alias';
import filesize from 'rollup-plugin-filesize';
import { terser } from "rollup-plugin-terser";
import commonjs from '@rollup/plugin-commonjs';
import resolve from "rollup-plugin-node-resolve"
import outputManifest from 'rollup-plugin-output-manifest';

export default {
    input: 'livewire/static/livewire/src/index.js',
    output: {
        format: 'umd',
        sourcemap: true,
        name: 'Livewire',
        file: 'livewire/static/livewire/dist/livewire.js',
    },
    plugins: [
        resolve(),
        commonjs({
            // These npm packages still use common-js modules. Ugh.
            include: /node_modules\/(get-value|isobject|core-js)/,
        }),
        filesize(),
        terser({
            mangle: false,
            compress: {
                drop_debugger: false,
            },
        }),
        babel({
            exclude: 'node_modules/**'
        }),
        alias({
            entries: [
                { find: '@', replacement: __dirname + '/livewire/static/livewire/src' },
            ]
        }),
        // Mimic Laravel Mix's mix-manifest file for auto-cache-busting.
        outputManifest({
            serialize() {
                const file = fs.readFileSync(__dirname + '/livewire/static/livewire/dist/livewire.js', 'utf8');
                const hash = md5(file).substr(0, 20);

                return JSON.stringify({
                    '/livewire.js': '/livewire.js?id=' + hash,
                })
            }
        }),
    ]
}
