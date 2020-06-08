module.exports = {
    configureWebpack: {
      devServer: {
          watchOptions: {
            ignored: ['node_modules'],
            aggregateTimeout: 300,
            poll: 1500
          },
          public: '147.100.102.68' // vagrant machine address
      }
    }
  }
