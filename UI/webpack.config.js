const path = require("path");
const webpack = require("webpack");
const BundleAnalyzerPlugin = require("webpack-bundle-analyzer").BundleAnalyzerPlugin;

module.exports = {
    entry: "./src/index.tsx",
    output: {
        path: path.resolve(__dirname, "./static/ui"),
        filename: "[name].js",
    },
    resolve: {
        extensions: [".js", ".jsx", ".json", ".ts", ".tsx"],
    },
    module: {
        rules: [
            {
                test: /\.js|.jsx$/,
                exclude: /node_modules/,
                // use: 'babel-loader',
                use: "babel-loader",
            },
            {
                test: /\.(ts|tsx)$/,
                loader: "ts-loader",
            },
            {
                test: /\.css$/,
                // include: path.resolve(__dirname, 'src'),
                use: ["style-loader", "css-loader", "postcss-loader"],
            },
        ],
    },
    optimization: {
        minimize: true,
    },
    plugins: [
        new webpack.DefinePlugin({
            "process.env": {
                NODE_ENV: JSON.stringify("development"),
                // NODE_ENV: JSON.stringify('production'),
            },
        }),
        // new BundleAnalyzerPlugin()
    ],
};
