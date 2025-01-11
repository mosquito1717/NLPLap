const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: { //Vue 개발 서버(8080) → Flask 서버(5000)로 API 요청 프록시 설정
    proxy: "http://localhost:5000",
  }
})
