import { readdirSync, statSync } from 'fs';
import { resolve, join, relative } from 'path';
import { defineConfig } from 'vite';

const CODE_OPTIMIZE = process.env.NODE_ENV === 'production';
const __dirname = resolve();

/**
 * Recursively scans directories for JS and CSS files
 * @param {string} dir - Directory to scan
 * @param {string[]} extensions - File extensions to include
 * @returns {string[]} Array of file paths
 */
function scanStaticFiles(dir, extensions = ['.js', '.css']) {
  const files = [];

  try {
    const entries = readdirSync(dir);

    for (const entry of entries) {
      const fullPath = join(dir, entry);
      const stat = statSync(fullPath);

      if (stat.isDirectory()) {
        files.push(...scanStaticFiles(fullPath, extensions));
      } else if (stat.isFile()) {
        const hasValidExtension = extensions.some((ext) => entry.endsWith(ext));
        if (hasValidExtension) {
          files.push(fullPath);
        }
      }
    }
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    console.warn(`Warning: Could not scan directory ${dir}:`, message);
  }

  return files;
}

/**
 * Generate entry points from static files
 * @returns {Record<string, string>} Entry points object
 */
function generateEntryPoints() {
  /** @type {Record<string, string>} */
  const entries = {};

  // Scan modules directory
  const modulesDir = resolve(__dirname, 'modules');
  const modulesFiles = scanStaticFiles(modulesDir);

  // Scan shared directory
  const sharedDir = resolve(__dirname, 'shared/static/shared');
  const sharedFiles = scanStaticFiles(sharedDir);

  // Process modules files
  for (const filePath of modulesFiles) {
    const relativePath = relative(__dirname, filePath);

    // Extract: modules/dish/static/dish/js/list.js → dish/js/list
    const match = relativePath.match(/modules\/([^/]+)\/static\/\1\/(.+)\.(js|css)$/);
    if (match) {
      const moduleName = match[1];
      const filePathInModule = match[2];
      const entryName = `${moduleName}/${filePathInModule}`;
      entries[entryName] = filePath;
    }
  }

  // Process shared files
  for (const filePath of sharedFiles) {
    const relativePath = relative(sharedDir, filePath);

    // Extract: js/main.js → shared/js/main
    // Extract: css/base.css → shared/css/base
    const entryName = `shared/${relativePath.replace(/\.(js|css)$/, '')}`;
    entries[entryName] = filePath;
  }

  console.log(`✨ Found ${Object.keys(entries).length} entry points:`);
  Object.keys(entries).forEach((key) => {
    console.log(`   - ${key}`);
  });

  return entries;
}

export default defineConfig({
  clearScreen: false,
  build: {
    minify: CODE_OPTIMIZE ? 'terser' : false,
    sourcemap: CODE_OPTIMIZE ? false : 'inline',
    target: 'es2021',
    outDir: 'staticfiles',
    emptyOutDir: false,
    terserOptions: {
      compress: CODE_OPTIMIZE,
      keep_classnames: true,
      keep_fnames: true,
    },
    rollupOptions: {
      treeshake: CODE_OPTIMIZE,
      input: generateEntryPoints(),
      output: {
        compact: CODE_OPTIMIZE,
        format: 'es',
        entryFileNames: (chunkInfo) => {
          return `${chunkInfo.name}.js`;
        },
        chunkFileNames: 'js/chunks/[name]-[hash].js',
        assetFileNames: (assetInfo) => {
          const name = assetInfo.name || '';

          // Handle CSS files
          if (name.endsWith('.css')) {
            // Keep the structure: shared/css/main.css, dish/css/list.css, etc.
            return name;
          }

          // Handle images and other assets
          if (/\.(png|jpe?g|svg|gif|webp|ico)$/i.test(name)) {
            return 'shared/images/[name]-[hash][extname]';
          }

          return 'assets/[name]-[hash][extname]';
        },
        manualChunks: (id) => {
          // Extract materialize-css into its own chunk
          if (id.includes('node_modules/materialize-css')) {
            return 'vendor/materialize';
          }
          // Group other node_modules into vendor chunk
          if (id.includes('node_modules')) {
            return 'vendor/libs';
          }
        },
      },
    },
    // Generate manifest for Django template integration
    manifest: true,
  },
  css: {
    postcss: {
      plugins: [],
    },
  },
  server: {
    origin: 'http://localhost:5173',
    port: 5173,
    strictPort: true,
    cors: true,
    hmr: {
      protocol: 'ws',
      host: 'localhost',
    },
  },
  preview: {
    port: 4173,
    strictPort: true,
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, './'),
      '@shared': resolve(__dirname, 'shared/static/shared'),
      '@dish': resolve(__dirname, 'modules/dish/static/dish'),
      '@category': resolve(__dirname, 'modules/category/static/category'),
    },
  },
  optimizeDeps: {
    include: ['materialize-css'],
  },
});
