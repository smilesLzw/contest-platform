<template>
  <div class="admin-ai-tools">
    <!-- Categories -->
    <section class="section">
      <div class="toolbar">
        <h3 class="section-label">分类管理</h3>
        <el-button size="default" @click="openCategoryDialog()">新增分类</el-button>
      </div>
      <el-table :data="categories">
        <el-table-column prop="name" label="分类名称" />
        <el-table-column prop="icon" label="图标" width="100" />
        <el-table-column prop="sort_order" label="排序" width="80" />
        <el-table-column label="操作" width="140">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="openCategoryDialog(row)">编辑</el-button>
            <el-button link size="small" @click="handleDeleteCategory(row)" style="color:var(--red)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </section>

    <!-- Tools -->
    <section class="section">
      <div class="toolbar">
        <h3 class="section-label">工具管理</h3>
        <el-button type="primary" size="default" @click="openToolDialog()">新增工具</el-button>
      </div>
      <el-table :data="tools">
        <el-table-column prop="name" label="工具名称" width="120" />
        <el-table-column prop="category_name" label="分类" width="100" />
        <el-table-column label="区域" width="70">
          <template #default="{ row }">{{ row.region === 'domestic' ? '国内' : '国外' }}</template>
        </el-table-column>
        <el-table-column prop="url" label="官网链接" min-width="180" show-overflow-tooltip />
        <el-table-column prop="description" label="简介" min-width="160" show-overflow-tooltip />
        <el-table-column label="免费" width="60">
          <template #default="{ row }">
            <span :class="['inline-tag', row.is_free ? 'yes' : 'no']">{{ row.is_free ? '是' : '否' }}</span>
          </template>
        </el-table-column>
        <el-table-column label="精选" width="60">
          <template #default="{ row }">
            <span v-if="row.is_featured" class="inline-tag featured">是</span>
            <span v-else style="color:var(--text-tertiary)">—</span>
          </template>
        </el-table-column>
        <el-table-column label="评分" width="70">
          <template #default="{ row }">★ {{ row.rating }}</template>
        </el-table-column>
        <el-table-column label="操作" width="140">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="openToolDialog(row)">编辑</el-button>
            <el-button link size="small" @click="handleDeleteTool(row)" style="color:var(--red)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination" v-if="toolsTotal > 0">
        <el-pagination
          v-model:current-page="toolsPage"
          v-model:page-size="toolsPageSize"
          :page-sizes="[20, 50]"
          :total="toolsTotal"
          layout="prev, pager, next, sizes, total"
          @current-change="loadTools"
          @size-change="loadTools"
        />
      </div>
    </section>

    <!-- Category dialog -->
    <el-dialog v-model="categoryDialog.visible" :title="categoryDialog.isEdit ? '编辑分类' : '新增分类'" width="400px">
      <el-form :model="categoryForm" label-width="72px">
        <el-form-item label="分类名称">
          <el-input v-model="categoryForm.name" />
        </el-form-item>
        <el-form-item label="图标">
          <el-input v-model="categoryForm.icon" placeholder="Element Plus 图标名" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="categoryForm.sort_order" :min="0" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="categoryDialog.visible = false">取消</el-button>
        <el-button type="primary" :loading="catSaving" @click="saveCategory">保存</el-button>
      </template>
    </el-dialog>

    <!-- Tool dialog -->
    <el-dialog v-model="toolDialog.visible" :title="toolDialog.isEdit ? '编辑工具' : '新增工具'" width="480px">
      <el-form :model="toolForm" label-width="72px">
        <el-form-item label="工具名称">
          <el-input v-model="toolForm.name" />
        </el-form-item>
        <el-form-item label="官网链接">
          <el-input v-model="toolForm.url" placeholder="https://" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="toolForm.category_id" style="width:100%">
            <el-option v-for="c in categories" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="区域">
          <el-select v-model="toolForm.region" style="width:100%">
            <el-option label="国内" value="domestic" />
            <el-option label="国外" value="international" />
          </el-select>
        </el-form-item>
        <el-form-item label="简介">
          <el-input v-model="toolForm.description" type="textarea" maxlength="300" show-word-limit />
        </el-form-item>
        <el-row :gutter="16">
          <el-col :span="8">
            <el-form-item label="免费">
              <el-switch v-model="toolForm.is_free" :active-value="1" :inactive-value="0" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="精选">
              <el-switch v-model="toolForm.is_featured" :active-value="1" :inactive-value="0" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="评分">
              <el-rate v-model="toolForm.rating" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <el-button @click="toolDialog.visible = false">取消</el-button>
        <el-button type="primary" :loading="toolSaving" @click="saveTool">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import {
  getCategories, createCategory, updateCategory, deleteCategory,
  getTools, createTool, updateTool, deleteTool,
} from '../../api/aiTools'
import { ElMessage, ElMessageBox } from 'element-plus'

const categories = ref([])
const tools = ref([])
const toolsTotal = ref(0)
const toolsPage = ref(1)
const toolsPageSize = ref(20)
const catSaving = ref(false)
const toolSaving = ref(false)

const categoryDialog = reactive({ visible: false, isEdit: false, editId: null })
const categoryForm = reactive({ name: '', icon: '', sort_order: 0 })

const toolDialog = reactive({ visible: false, isEdit: false, editId: null })
const toolForm = reactive({
  name: '', url: '', category_id: null, description: '',
  region: 'domestic', is_free: 1, is_featured: 0, rating: 5, sort_order: 0, logo_url: '',
})

function openCategoryDialog(row) {
  if (row) {
    categoryDialog.isEdit = true; categoryDialog.editId = row.id
    categoryForm.name = row.name; categoryForm.icon = row.icon || ''; categoryForm.sort_order = row.sort_order
  } else {
    categoryDialog.isEdit = false; categoryDialog.editId = null
    categoryForm.name = ''; categoryForm.icon = ''; categoryForm.sort_order = 0
  }
  categoryDialog.visible = true
}

async function saveCategory() {
  catSaving.value = true
  try {
    if (categoryDialog.isEdit) {
      await updateCategory(categoryDialog.editId, { ...categoryForm }); ElMessage.success('更新成功')
    } else {
      await createCategory({ ...categoryForm }); ElMessage.success('创建成功')
    }
    categoryDialog.visible = false; loadData()
  } catch (e) { console.error(e) }
  finally { catSaving.value = false }
}

async function handleDeleteCategory(row) {
  try {
    await ElMessageBox.confirm(`确定删除分类"${row.name}"？`, '删除确认', { type: 'warning' })
    await deleteCategory(row.id); ElMessage.success('删除成功'); loadData()
  } catch (e) { if (e !== 'cancel') console.error(e) }
}

function openToolDialog(row) {
  if (row) {
    toolDialog.isEdit = true; toolDialog.editId = row.id
    Object.assign(toolForm, {
      name: row.name, url: row.url, category_id: row.category_id,
      description: row.description || '', region: row.region || 'domestic',
      is_free: row.is_free, is_featured: row.is_featured, rating: row.rating,
      sort_order: row.sort_order, logo_url: row.logo_url || '',
    })
  } else {
    toolDialog.isEdit = false; toolDialog.editId = null
    Object.assign(toolForm, {
      name: '', url: '', category_id: null, description: '',
      region: 'domestic', is_free: 1, is_featured: 0, rating: 5, sort_order: 0, logo_url: '',
    })
  }
  toolDialog.visible = true
}

async function saveTool() {
  toolSaving.value = true
  try {
    if (toolDialog.isEdit) {
      await updateTool(toolDialog.editId, { ...toolForm }); ElMessage.success('更新成功')
    } else {
      await createTool({ ...toolForm }); ElMessage.success('创建成功')
    }
    toolDialog.visible = false; loadData()
  } catch (e) { console.error(e) }
  finally { toolSaving.value = false }
}

async function handleDeleteTool(row) {
  try {
    await ElMessageBox.confirm(`确定删除工具"${row.name}"？`, '删除确认', { type: 'warning' })
    await deleteTool(row.id); ElMessage.success('删除成功'); loadData()
  } catch (e) { if (e !== 'cancel') console.error(e) }
}

async function loadData() {
  try {
    const [catRes, toolsRes] = await Promise.all([
      getCategories(),
      getTools({ page: toolsPage.value, page_size: toolsPageSize.value }),
    ])
    categories.value = catRes.data || []
    tools.value = toolsRes.data?.items || []
    toolsTotal.value = toolsRes.data?.total || 0
  } catch (e) { console.error(e) }
}

function loadTools() {
  loadData()
}

onMounted(loadData)
</script>

<style scoped>
.section { margin-bottom: 36px; }
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}
.section-label {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

.inline-tag {
  font-size: 11px;
  font-weight: 500;
  padding: 1px 6px;
  border-radius: 6px;
}
.inline-tag.yes { background: rgba(52, 199, 89, 0.1); color: var(--green); }
.inline-tag.no { background: rgba(134, 134, 139, 0.06); color: var(--text-tertiary); }
.inline-tag.featured { background: rgba(0, 113, 227, 0.08); color: var(--accent); }

.pagination { display: flex; justify-content: center; margin-top: 20px; }
</style>
