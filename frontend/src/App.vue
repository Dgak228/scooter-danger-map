<script>
import RouteMap from './components/RouteMap.vue'

export default {
  name: 'App',
  components: {
    RouteMap
  }
}
</script>

<template>
  <div id="app">
    <RouteMap />
  </div>
</template>

<style>
#app {
  font-family: Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  width: 100%;
  height: 100vh;
  margin: 0;
  padding: 0;
}

body {
  margin: 0;
  padding: 0;
}

.main-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 64px;
  background: #fff;
  box-shadow: 0 2px 8px #f0f1f2;
  z-index: 100;
  display: flex;
  align-items: center;
  padding: 0 32px;
  justify-content: space-between;
}
.site-title {
  margin: 0;
  font-weight: 700;
  font-size: 1.35rem;
  color: #222;
  letter-spacing: 0.01em;
  line-height: 64px;
}
.main-nav {
  display: flex;
  gap: 24px;
}
.nav-link {
  color: #222;
  text-decoration: none;
  font-weight: 500;
  font-size: 1.1rem;
  padding: 6px 18px;
  border-radius: 6px;
  transition: background 0.2s, color 0.2s;
}
.nav-link.active, .nav-link.router-link-exact-active {
  background: #409eff;
  color: #fff;
}
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding-top: 80px;
  padding-bottom: 40px;
  min-height: 100vh;
}
.main-row {
  margin-left: 0 !important;
  margin-right: 0 !important;
}
.map-placeholder {
  height: 400px;
  background: linear-gradient(135deg, #e0e7ef 0%, #f5f7fa 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #bbb;
  font-size: 1.2rem;
  border-radius: 8px;
  border: 1px dashed #d3dce6;
  margin-bottom: 8px;
}
.el-card {
  border-radius: 10px;
}
@media (max-width: 600px) {
  .main-header {
    height: 48px;
    padding: 0 8px;
  }
  .site-title {
    font-size: 1rem;
    line-height: 48px;
  }
  .main-content {
    padding-top: 56px;
  }
  .main-nav {
    gap: 8px;
  }
  .nav-link {
    font-size: 0.95rem;
    padding: 4px 10px;
  }
}
</style>
