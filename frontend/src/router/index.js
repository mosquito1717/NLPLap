import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/HomeView.vue'
import Search from '@/views/SearchView.vue'
import Upload from '@/views/UploadView.vue'

const routes =[
    // path: URL 경로
    // name: 라우트 이름 (선택 사항)
    // component: 연결된 컴포넌트    
    { path: '/', name: 'Home', component: Home},
    { path: '/search', name: 'Search', component: Search},
    { path: '/upload', name: 'Upload', component: Upload}
]

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;