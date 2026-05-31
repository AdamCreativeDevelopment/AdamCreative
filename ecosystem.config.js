// ecosystem.config.js
// PM2 process manager configuration for the Adam Creative Studios bot network.
// Usage:
//   Start all bots:   pm2 start ecosystem.config.js
//   Stop all bots:    pm2 stop all
//   View dashboard:   pm2 monit
//   Restart one bot:  pm2 restart acs-core

module.exports = {
  apps: [
    {
      name:          "acs-core",
      script:        "./bots/core_bot/main.py",
      interpreter:   "python3",
      restart_delay: 5000,
      max_restarts:  10,
      watch:         false,
      env: {
        PYTHONPATH: "."
      },
      log_file:      "./logs/core.log",
      error_file:    "./logs/core_error.log",
      time:          true,
    },
    {
      name:          "acs-staff",
      script:        "./bots/staff_bot/main.py",
      interpreter:   "python3",
      restart_delay: 5000,
      max_restarts:  10,
      watch:         false,
      env: {
        PYTHONPATH: "."
      },
      log_file:      "./logs/staff.log",
      error_file:    "./logs/staff_error.log",
      time:          true,
    },
    {
      name:          "acs-design",
      script:        "./bots/design_bot/main.py",
      interpreter:   "python3",
      restart_delay: 5000,
      max_restarts:  10,
      watch:         false,
      env: {
        PYTHONPATH: "."
      },
      log_file:      "./logs/design.log",
      error_file:    "./logs/design_error.log",
      time:          true,
    },
    {
      name:          "acs-dev",
      script:        "./bots/dev_bot/main.py",
      interpreter:   "python3",
      restart_delay: 5000,
      max_restarts:  10,
      watch:         false,
      env: {
        PYTHONPATH: "."
      },
      log_file:      "./logs/dev.log",
      error_file:    "./logs/dev_error.log",
      time:          true,
    },
    {
      name:          "acs-customs",
      script:        "./bots/customs_bot/main.py",
      interpreter:   "python3",
      restart_delay: 5000,
      max_restarts:  10,
      watch:         false,
      env: {
        PYTHONPATH: "."
      },
      log_file:      "./logs/customs.log",
      error_file:    "./logs/customs_error.log",
      time:          true,
    },
  ]
};
