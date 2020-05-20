module.exports = {
    configureWebpack: {
      devServer: {
          watchOptions: {
            ignored: ['node_modules'],
            aggregateTimeout: 300,
            poll: 1500
          },
          public: '0.0.0.0' // vagrant machine address
      }
    }
  }