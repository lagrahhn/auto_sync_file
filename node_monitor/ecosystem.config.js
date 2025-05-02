module.exports = {
  apps: [{
    name: 'markdown-sync',
    script: 'index.js',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '200M',
    env: {
      NODE_ENV: 'production',
      DEBUG: 'false'
    },
    env_development: {
      NODE_ENV: 'development',
      DEBUG: 'true'
    }
  }]
}; 