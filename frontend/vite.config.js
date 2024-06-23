import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";
import terminal from "vite-plugin-terminal";

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        react(),
        terminal({
            console: "terminal",
            output: ["terminal", "console"],
        }),
    ],
});
