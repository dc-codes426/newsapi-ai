# NewsAPI AI - Web Frontend

A modern, responsive website built with React and Vite, inspired by newsapi.org.

## Features

- Clean, developer-focused UI
- Interactive code examples with syntax highlighting
- Responsive design that works on all devices
- Fast development with Vite and Hot Module Replacement (HMR)

## Getting Started

### Prerequisites

- Node.js 16+ installed

### Installation

```bash
# Install dependencies
npm install
```

### Development

```bash
# Start development server
npm run dev
```

The site will be available at `http://localhost:3000`

### Build for Production

```bash
# Create production build
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
web/
├── src/
│   ├── components/
│   │   ├── Header.jsx          # Navigation bar
│   │   ├── Hero.jsx            # Hero section with CTA
│   │   ├── CodeExamples.jsx    # Interactive API examples
│   │   ├── Features.jsx        # Feature cards and CTA
│   │   └── Footer.jsx          # Footer links
│   ├── App.jsx                 # Main app component
│   ├── main.jsx               # Entry point
│   └── index.css              # Global styles
├── index.html                 # HTML template
├── package.json               # Dependencies
└── vite.config.js            # Vite configuration
```

## Technologies Used

- React 18
- Vite 5
- CSS3 (no CSS frameworks for maximum customization)
- Google Fonts (Inter)
