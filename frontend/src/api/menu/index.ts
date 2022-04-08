import request from '/@/utils/request';

/**
 * 获取后端动态路由菜单
 * @link 参考：https://gitee.com/lyt-top/vue-next-admin-images/tree/master/menu
 * @param params 要传的参数值，非必传
 * @returns 返回接口数据
 */
export function getMenu(params?: object) {
	return request({
		url: '/user/getMenu',
		method: 'get',
		params,
	});
}
