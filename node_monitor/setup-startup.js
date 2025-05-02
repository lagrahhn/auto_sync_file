#!/usr/bin/env node

const { exec } = require('child_process');
const os = require('os');

/**
 * 执行命令
 * @param {string} command - 要执行的命令
 * @returns {Promise<string>} - 命令输出
 */
function executeCommand(command) {
  return new Promise((resolve, reject) => {
    console.log(`执行命令: ${command}`);
    exec(command, (error, stdout, stderr) => {
      if (error) {
        console.error(`执行命令失败: ${error.message}`);
        if (stderr) console.error(stderr);
        reject(error);
        return;
      }
      if (stdout) console.log(stdout);
      resolve(stdout.trim());
    });
  });
}

/**
 * 获取操作系统类型
 * @returns {string} - 操作系统类型 (windows|linux|macos)
 */
function getOsType() {
  const platform = os.platform();
  if (platform === 'win32') return 'windows';
  if (platform === 'darwin') return 'macos';
  return 'linux';
}

/**
 * 配置PM2开机自启动
 */
async function setupStartup() {
  console.log('=== 配置PM2开机自启动 ===');

  try {
    // 检查PM2是否已安装
    try {
      await executeCommand('pm2 --version');
    } catch (error) {
      console.log('PM2未安装，正在安装...');
      await executeCommand('npm install pm2 -g');
    }

    // 启动应用
    console.log('启动应用...');
    await executeCommand('pm2 start ecosystem.config.js');
    
    // 保存当前运行的应用
    console.log('保存当前运行的应用...');
    await executeCommand('pm2 save');
    
    // 获取开机自启动命令
    console.log('获取开机自启动命令...');
    const osType = getOsType();
    console.log(`检测到操作系统类型: ${osType}`);
    
    // 生成并执行开机自启动命令
    let startupCommand;
    if (osType === 'windows') {
      // Windows平台使用特定的启动脚本
      console.log('在Windows上配置开机自启动...');
      
      // 获取PM2启动命令
      startupCommand = await executeCommand('pm2 startup');
      console.log('\n请手动复制并以管理员身份运行上面生成的命令。');
      console.log('或者运行以下命令创建计划任务:');
      console.log('schtasks /create /tn "PM2 Auto Sync" /sc onlogon /ru SYSTEM /tr "pm2 resurrect"');
    } else {
      // Linux/MacOS平台
      startupCommand = await executeCommand('pm2 startup');
      
      // 从输出中提取需要执行的命令
      const match = startupCommand.match(/sudo\s+.+/);
      if (match) {
        const sudoCommand = match[0];
        console.log(`\n请执行以下命令完成开机自启动配置:`);
        console.log(sudoCommand);
        
        // 尝试自动执行
        try {
          await executeCommand(sudoCommand);
          console.log('开机自启动配置完成！');
        } catch (error) {
          console.log('无法自动执行sudo命令，请手动执行上述命令。');
        }
      } else {
        console.log('无法解析启动命令，请查看上面的输出并手动执行相应命令。');
      }
    }
    
    console.log('\n=== 配置完成 ===');
    console.log('您可以通过以下命令管理服务:');
    console.log('- 查看状态: pm2 status');
    console.log('- 查看日志: pm2 logs markdown-sync');
    console.log('- 停止服务: pm2 stop markdown-sync');
    console.log('- 重启服务: pm2 restart markdown-sync');
    console.log('- 监控: pm2 monit');
  } catch (error) {
    console.error('配置过程中发生错误:', error);
  }
}

// 开始配置
setupStartup(); 