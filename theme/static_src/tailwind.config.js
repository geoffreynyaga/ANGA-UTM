/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

/* Colours are defined as CSS variables in src/styles.css. */
const token = (name) => `rgb(var(--color-${name}) / <alpha-value>)`;

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /* React screens served under /ui/ use the same stylesheet. */
        '../../ui/src/**/*.{js,jsx,ts,tsx}',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {
            colors: {
                brand: {
                    DEFAULT: token('brand'),
                    hover: token('brand-hover'),
                    strong: token('brand-strong'),
                    soft: token('brand-soft'),
                    ring: token('brand-ring'),
                },
                accent: {
                    DEFAULT: token('accent'),
                    soft: token('accent-soft'),
                    strong: token('accent-strong'),
                },
                success: {
                    DEFAULT: token('success'),
                    soft: token('success-soft'),
                    strong: token('success-strong'),
                },
                danger: {
                    DEFAULT: token('danger'),
                    soft: token('danger-soft'),
                },
                ink: {
                    DEFAULT: token('ink'),
                    label: token('ink-label'),
                    body: token('ink-body'),
                    muted: token('ink-muted'),
                    subtle: token('ink-subtle'),
                    faint: token('ink-faint'),
                },
                line: {
                    DEFAULT: token('line'),
                    input: token('line-input'),
                    soft: token('line-soft'),
                    dashed: token('line-dashed'),
                },
                surface: {
                    page: token('surface-page'),
                    subtle: token('surface-subtle'),
                    hover: token('surface-hover'),
                    track: token('surface-track'),
                    chip: token('surface-chip'),
                },
                sidebar: {
                    DEFAULT: token('sidebar'),
                    text: token('sidebar-text'),
                    active: token('sidebar-active'),
                    hover: token('sidebar-hover'),
                },
            },
            fontFamily: {
                sans: ['Manrope', 'system-ui', 'sans-serif'],
                display: ['Michroma', 'sans-serif'],
                mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
            },
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
