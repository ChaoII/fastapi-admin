<template>
	<div class="system-edit-user-container">
		<el-dialog title="修改用户" v-model="isShowDialog" width="769px">
			<el-form :model="ruleForm" size="small" label-width="90px">
				<el-row :gutter="35">
					<el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
						<el-form-item label="用户名">
							<el-input v-model="ruleForm.name" placeholder="请输入账户名称" clearable></el-input>
						</el-form-item>
					</el-col>
					<el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
						<el-form-item label="昵称">
							<el-input v-model="ruleForm.nicename" placeholder="请输入用户昵称" clearable></el-input>
						</el-form-item>
					</el-col>
					<el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
						<el-form-item label="角色">
							<el-select v-model="ruleForm.role" placeholder="请选择" clearable class="w100">
								<el-option label="超级管理员" value="admin"></el-option>
								<el-option label="普通用户" value="user"></el-option>
							</el-select>
						</el-form-item>
					</el-col>
					<el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" class="mb20">
						<el-form-item label="用户状态">
							<el-switch v-model="ruleForm.status" inline-prompt active-text="启" inactive-text="禁"></el-switch>
						</el-form-item>
					</el-col>
				</el-row>
			</el-form>
			<template #footer>
				<span class="dialog-footer">
					<el-button @click="onCancel" size="small">取 消</el-button>
					<el-button type="primary" @click="onSubmit" size="small">修 改</el-button>
				</span>
			</template>
		</el-dialog>
	</div>
</template>

<script lang="ts">
import { reactive, toRefs, onMounted } from 'vue';
import request from '/@/utils/request';
import { ElMessage } from 'element-plus';
export default {
	name: 'systemEditUser',
	emits:['refdata'],
	setup(props,{attrs,slots,emit}) {
		const state = reactive({
			isShowDialog: false,
			ruleForm: {
				id:'',
				username: '', // 账户名称
				nicename: '', // 用户昵称
				role: '', // 关联角色
				password: '', // 账户密码
				status: '', // 用户状态
			},
			deptData: [], // 部门数据
		});
		// 打开弹窗
		const openDialog = (row: Object) => {
			state.ruleForm = row;
			state.ruleForm.status=state.ruleForm.status==1?true:false
			state.isShowDialog = true;
		};
		// 关闭弹窗
		const closeDialog = () => {
			state.isShowDialog = false;
		};
		// 取消
		const onCancel = () => {
			closeDialog();
		};
		// 新增
		const onSubmit = async () => {
			await request({
				url: '/user/editUser',
				method: 'POST',
				data: state.ruleForm,
			});
			emit('refdata')
			ElMessage.success(`用户：${state.ruleForm.username}添加成功`);
			closeDialog();
		};
		// 页面加载时
		onMounted(() => {
		});
		return {
			openDialog,
			closeDialog,
			onCancel,
			onSubmit,
			...toRefs(state),
		};
	},
};
</script>
