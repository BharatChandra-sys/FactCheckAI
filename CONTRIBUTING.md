<!-- Copyright 2027 Bodapati Bharat Chandra. All rights reserved. -->
<!-- Licensed under the Apache License, Version 2.0 | SPDX-License-Identifier: Apache-2.0 -->

# Contributing to FactCheckAI

We welcome contributions from the community! This guide will help you get started with contributing to FactCheckAI.

## 🚀 Quick Start

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/fake-news-extension.git
   cd fake-news-extension
   ```

2. **Set up development environment**
   ```bash
   # Backend setup
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

3. **Run tests**
   ```bash
   pytest tests/ -v --cov=app
   ```

## 📋 Development Guidelines

### Code Standards
- **Python**: Follow PEP 8, use type hints, docstrings for public functions
- **JavaScript**: ES6+, consistent naming, JSDoc for complex functions  
- **Test Coverage**: Minimum 90% for new code
- **Performance**: No regressions in API response times

### Commit Convention
We use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add multimodal analysis support
fix: resolve JWT token expiration issue  
docs: update API documentation
test: add integration tests for ML routing
perf: optimize database query performance
refactor: simplify authentication middleware
```

### Branch Strategy
- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/description` - New features
- `fix/description` - Bug fixes
- `hotfix/description` - Critical production fixes

## 🧪 Testing Requirements

### Backend Testing
```bash
# Unit tests
pytest tests/unit/ -v

# Integration tests  
pytest tests/integration/ -v

# Load testing
locust -f tests/load_test.py --host=http://localhost:8000

# Security testing
bandit -r app/
safety check
```

### Extension Testing
```bash
cd extension
npm install
npm test
npm run test:e2e
```

### ML Model Testing
```bash
# Model accuracy validation
python tests/test_ml_accuracy.py

# Performance benchmarking
python tests/benchmark_ml_performance.py
```

## 🔒 Security Guidelines

### Sensitive Data
- Never commit API keys, passwords, or secrets
- Use environment variables for configuration
- Sanitize all user inputs
- Follow OWASP security guidelines

### Code Review Checklist
- [ ] No hardcoded secrets or credentials
- [ ] Input validation and sanitization  
- [ ] Error handling without information leakage
- [ ] Performance impact assessed
- [ ] Tests cover edge cases
- [ ] Documentation updated

## 🎯 Areas for Contribution

### High Priority
- **ML Model Improvements**: Better accuracy, faster inference
- **Multi-language Support**: Translation and localization
- **Performance Optimization**: Caching, query optimization
- **Security Enhancements**: Additional authentication methods

### Medium Priority  
- **UI/UX Improvements**: Better user experience
- **API Enhancements**: New endpoints, better documentation
- **Integration Support**: New platform connectors
- **Monitoring & Analytics**: Better observability

### Documentation
- Code examples and tutorials
- Architecture documentation
- Deployment guides
- API reference improvements

## 📝 Pull Request Process

1. **Create feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes with tests**
   - Write code following our standards
   - Add comprehensive tests
   - Update documentation

3. **Run validation**
   ```bash
   # Run full test suite
   make test-all
   
   # Check code quality
   make lint
   ```

4. **Submit pull request**
   - Clear title and description
   - Reference related issues
   - Include performance impact
   - Add screenshots for UI changes

5. **Code review process**
   - Automated checks must pass
   - At least 2 reviewer approvals
   - Performance regression testing
   - Security review for sensitive changes

## 🐛 Bug Reports

### Before Reporting
- Search existing issues
- Test with latest version
- Reproduce with minimal example

### Bug Report Template
```markdown
**Description**
Clear description of the bug

**Steps to Reproduce**
1. Go to...
2. Click on...
3. See error

**Expected Behavior**
What should happen

**Actual Behavior**  
What actually happens

**Environment**
- Browser: Chrome 120
- Extension version: 2.6.1
- OS: Windows 11

**Additional Context**
Screenshots, console logs, etc.
```

## 💡 Feature Requests

### Feature Request Template
```markdown
**Problem Statement**
What problem does this solve?

**Proposed Solution**
How would you like it to work?

**Alternatives Considered**
Other approaches you've thought about

**Impact**
Who benefits and how?

**Implementation Notes**
Technical considerations, if any
```

## 📚 Development Resources

### Architecture Overview
- [INFRASTRUCTURE_PLAN.md](INFRASTRUCTURE_PLAN.md) - Deployment architecture
- `backend/app/` - FastAPI application structure
- `extension/` - Chrome extension code

### Key Technologies
- **Backend**: FastAPI, SQLAlchemy, Alembic, PyTorch
- **Database**: PostgreSQL with FTS5 search
- **ML**: Transformers, scikit-learn, custom models  
- **Infrastructure**: Multi-cloud (Render, Heroku, Azure, HF)

### Local Development URLs
- API Server: http://localhost:8000
- API Docs: http://localhost:8000/docs  
- Health Check: http://localhost:8000/health

## 🏆 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Invited to contributor Discord channel
- Eligible for contributor swag

## ❓ Getting Help

- **Discord**: Real-time chat with maintainers
- **GitHub Discussions**: Design discussions, Q&A
- **Email**: technical@factcheckai.com for sensitive issues

## 📄 License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.