#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Setting up Real-Time Code Complexity Analyzer...${NC}"

# Create project structure
echo -e "${GREEN}Creating project structure...${NC}"
mkdir -p code-complexity-analyzer
cd code-complexity-analyzer
mkdir -p src/{analyzers,visualizers,utils} tests/{unit,integration} docs

# Initialize npm project
echo -e "${GREEN}Initializing npm project...${NC}"
npm init -y

# Create necessary files
echo -e "${GREEN}Creating project files...${NC}"
touch src/cli.js
touch src/analyzers/{complexity.js,metrics.js,parser.js}
touch src/visualizers/{wolfram.js,chart.js}
touch src/utils/{file-handler.js,logger.js}
touch .env.example
touch .gitignore

# Update package.json with dependencies
echo -e "${GREEN}Adding dependencies...${NC}"
npm install --save \
    @babel/parser \
    @babel/traverse \
    axios \
    commander \
    dotenv \
    chalk \
    ora \
    wolframalpha-api-node

# Add dev dependencies
npm install --save-dev \
    jest \
    eslint \
    prettier \
    @babel/core \
    @types/jest

# Make CLI executable
chmod +x src/cli.js

# Create .gitignore
cat > .gitignore << EOL
node_modules/
.env
coverage/
dist/
.DS_Store
*.log
EOL

# Create .env.example
cat > .env.example << EOL
WOLFRAM_API_KEY=your_wolfram_api_key_here
DASHBOARD_URL=https://dashboard.codepulse.xyz
EOL

# Create basic test setup
cat > tests/unit/complexity.test.js << EOL
describe('Complexity Analyzer', () => {
    test('should calculate cyclomatic complexity', () => {
        // Add your test here
    });
});
EOL

# Add npm scripts to package.json
npm pkg set scripts.start="node src/cli.js"
npm pkg set scripts.test="jest"
npm pkg set scripts.lint="eslint src/**/*.js"
npm pkg set scripts.format="prettier --write 'src/**/*.js'"
npm pkg set scripts.build="babel src -d dist"

# Initialize Git repository
echo -e "${GREEN}Initializing Git repository...${NC}"
git init
git add .
git commit -m "Initial commit: Project setup"

echo -e "${BLUE}✨ Setup complete! Next steps:${NC}"
echo -e "1. Add your Wolfram API key to .env file"
echo -e "2. Run 'npm install' to install dependencies"
echo -e "3. Start developing with 'npm start'"
echo -e "4. Run tests with 'npm test'"

# Create a basic README
cat > README.md << EOL
# Real-Time Code Complexity Analyzer

A powerful developer tool that provides instant insights into code complexity and quality metrics, powered by advanced algorithms and beautiful visualizations.

## Features

- Real-time analysis of code complexity metrics
- Interactive visualizations powered by Wolfram API
- Detailed reports with actionable insights
- CLI tool for seamless integration
- Web dashboard for team collaboration

## Quick Start

\`\`\`bash
# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the analyzer
npm start <path-to-project>
\`\`\`

## Development

\`\`\`bash
# Run tests
npm test

# Lint code
npm run lint

# Format code
npm run format
\`\`\`

## Sponsors

- **Code Crafters** - Empowering our core analysis engine
- **Wolfram** - Providing advanced computational and visualization capabilities
- **.xyz** - Hosting our platform at [codepulse.xyz](https://codepulse.xyz)

## License

MIT
EOL

# Create ESLint config
cat > .eslintrc.json << EOL
{
    "env": {
        "node": true,
        "es2021": true,
        "jest": true
    },
    "extends": "eslint:recommended",
    "parserOptions": {
        "ecmaVersion": "latest",
        "sourceType": "module"
    },
    "rules": {
        "indent": ["error", 4],
        "linebreak-style": ["error", "unix"],
        "quotes": ["error", "single"],
        "semi": ["error", "always"]
    }
}
EOL

# Create Prettier config
cat > .prettierrc << EOL
{
    "semi": true,
    "trailingComma": "es5",
    "singleQuote": true,
    "printWidth": 100,
    "tabWidth": 4
}
EOL

# Create Jest config
cat > jest.config.js << EOL
module.exports = {
    testEnvironment: 'node',
    coverageDirectory: 'coverage',
    collectCoverageFrom: ['src/**/*.js'],
    testMatch: ['**/tests/**/*.test.js'],
};
EOL

echo -e "${BLUE}🎉 Project setup complete! Happy coding!${NC}" 