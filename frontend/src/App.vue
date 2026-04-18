<template>
  <div id="app">
    <el-container style="min-height: 100vh">
      <el-aside width="220px" style="background: #001529">
        <div class="logo-title">Lab Equipment System</div>
        <el-menu
          :default-active="$route.path"
          router
          background-color="#001529"
          text-color="rgba(255,255,255,0.65)"
          active-text-color="#fff"
        >
          <el-menu-item index="/equipment">
            <el-icon><Tools /></el-icon>
            <span>Equipment</span>
          </el-menu-item>
          <el-menu-item index="/usage">
            <el-icon><List /></el-icon>
            <span>Usage Records</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header style="display: flex; align-items: center; justify-content: space-between; background: #fff; border-bottom: 1px solid #e8e8e8">
          <span style="font-size: 18px; font-weight: bold; color: #333">Laboratory Equipment System</span>
          <el-tag type="success">Basic v1.0</el-tag>
        </el-header>
        <el-main style="background: #f0f2f5; padding: 20px">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { Tools, List } from '@element-plus/icons-vue'
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
#app { height: 100vh; font-family: "Microsoft YaHei", Arial, sans-serif; }
.logo-title {
  height: 60px;
  line-height: 60px;
  text-align: center;
  color: #fff;
  font-size: 15px;
  font-weight: bold;
  letter-spacing: 1px;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}
</style>
