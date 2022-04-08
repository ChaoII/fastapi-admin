<template>
	<div class="system-user-container">
		<el-card shadow="hover">
			<div class="system-user-search mb15">
				<el-input size="small" v-model="searstr" placeholder="请输入用户名称" style="max-width: 180px"> </el-input>
				<el-button size="small" type="primary" class="ml10" @click="initTableData">
					<el-icon>
						<elementSearch />
					</el-icon>
					查询
				</el-button>
				<el-button size="small" type="success" class="ml10" @click="onOpenAddUser">
					<el-icon>
						<elementFolderAdd />
					</el-icon>
					新增用户
				</el-button>
			</div>
			<el-table :data="tableData.data" style="width: 100%">
				<el-table-column prop="id" label="序号" width="50" />
				<el-table-column prop="name" label="用户名" show-overflow-tooltip width="80"></el-table-column>
				<el-table-column prop="nicename" label="昵称" show-overflow-tooltip></el-table-column>
				<el-table-column prop="role" label="角色" show-overflow-tooltip>
					<template #default="scope">
						<div  v-if="scope.row.role=='admin'">管理员</div>
						<div  v-else>普通用户</div>
					</template>
				</el-table-column>

				<el-table-column prop="create" label="创建时间" show-overflow-tooltip></el-table-column>
				<el-table-column prop="create" label="最后登录" show-overflow-tooltip></el-table-column>
				<el-table-column prop="status" label="用户状态" show-overflow-tooltip>
					<template #default="scope">
						<el-tag type="success" v-if="scope.row.status">启用</el-tag>
						<el-tag type="info" v-else>禁用</el-tag>
					</template>
				</el-table-column>
				<el-table-column label="操作" width="100">
					<template #default="scope">
						<el-button :disabled="scope.row.name === 'admin'" size="mini" type="text" @click="onOpenEditUser(scope.row)">修改</el-button>
						<el-button :disabled="scope.row.name === 'admin'" size="mini" type="text" @click="onRowDel(scope.row)">删除</el-button>
					</template>
				</el-table-column>
			</el-table>
			<el-pagination
				@size-change="onHandleSizeChange"
				@current-change="onHandleCurrentChange"
				class="mt15"
				:pager-count="5"
				:page-sizes="[10, 20, 30]"
				v-model:current-page="tableData.param.pageNum"
				background
				v-model:page-size="tableData.param.pageSize"
				layout="total, sizes, prev, pager, next, jumper"
				:total="tableData.total"
			>
			</el-pagination>
		</el-card>
		<AddUer ref="addUserRef" @refdata="initTableData" />
		<EditUser ref="editUserRef" />
	</div>
</template>

<script lang="ts">
import { toRefs, reactive, onMounted, ref } from 'vue';
import { ElMessageBox, ElMessage } from 'element-plus';
import AddUer from '/@/views/system/user/component/addUser.vue';
import EditUser from '/@/views/system/user/component/editUser.vue';
import request from '/@/utils/request';
export default {
	name: 'systemUser',
	components: { AddUer, EditUser },
	setup() {
		const addUserRef = ref();
		const editUserRef = ref();
		const state: any = reactive({
			searstr:'',
			tableData: {
				data: [],
				total: 0,
				loading: false,
				param: {
					pageNum: 1,
					pageSize: 10,
				},
			},
		});
		// 初始化表格数据
		const initTableData = async(searstr='') => {
			const data= await request({
				url: '/user/getUser',
				method: 'GET',
				params: {searstr:state.searstr},
			});
			state.tableData.data = data.user;
			state.tableData.total = data.total;
		};
		// 打开新增用户弹窗
		const onOpenAddUser = () => {
			addUserRef.value.openDialog();
		};
		// 打开修改用户弹窗
		const onOpenEditUser = (row: Object) => {
			editUserRef.value.openDialog(row);
		};
		// 删除用户
		const onRowDel = (row: Object) => {
			ElMessageBox.confirm(`此操作将永久删除账户名称：“${row.name}”，是否继续?`, '提示', {
				confirmButtonText: '确认',
				cancelButtonText: '取消',
				type: 'warning',
			}).then(() => {
					request({
						url: '/user/delUser',
						method: 'POST',
						data: row.id,
					});
				initTableData();
				})
				.catch(() => {});
		};
		// 分页改变
		const onHandleSizeChange = (val: number) => {
			state.tableData.param.pageSize = val;
		};
		// 分页改变
		const onHandleCurrentChange = (val: number) => {
			state.tableData.param.pageNum = val;
		};
		// 页面加载时
		onMounted(() => {
			initTableData();
		});
		return {
			addUserRef,
			editUserRef,
			onOpenAddUser,
			onOpenEditUser,
			onRowDel,
			onHandleSizeChange,
			onHandleCurrentChange,
			initTableData,
			...toRefs(state),
		};
	},
};
</script>

<style scoped lang="scss">
.system-user-container {
}
</style>
