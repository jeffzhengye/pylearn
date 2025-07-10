import os
import open3d as o3d
import pyassimp


def convert_fbx_to_obj(fbx_path, obj_path):
    """
    将FBX文件转换为OBJ文件
    :param fbx_path: FBX文件的路径
    :param obj_path: 转换后OBJ文件的保存路径
    """
    if not os.path.exists(fbx_path):
        print(f"指定的FBX文件不存在: {fbx_path}")
        return
    try:
        with pyassimp.load(fbx_path) as scene:
            print("FBX文件加载成功，检查场景对象是否有效")
            if scene is None:
                print("加载的场景对象为空")
                return
            # 打印场景中的网格数量，用于调试
            print(f"场景中的网格数量: {len(scene.meshes)}")
            try:
                pyassimp.export(scene, obj_path, file_type='obj')
                print(f"成功将FBX文件转换为OBJ文件，保存路径: {obj_path}")
            except Exception as e:
                print(f"导出OBJ文件时出错: {e}")
    except Exception as e:
        print(f"加载或处理FBX文件时出错: {e}")


def display_obj_with_open3d(obj_path):
    """
    使用Open3D显示OBJ文件
    :param obj_path: OBJ文件的路径
    """
    mesh = o3d.io.read_triangle_mesh(obj_path)
    mesh.compute_vertex_normals()
    o3d.visualization.draw_geometries([mesh])


if __name__ == "__main__":
    fbx_file = 'd:/wps/公司项目/数字人/陈琦/女生走路.fbx'
    temp_obj_file = 'temp.obj'

    if os.path.exists(fbx_file):
        convert_fbx_to_obj(fbx_file, temp_obj_file)
        if os.path.exists(temp_obj_file):
            display_obj_with_open3d(temp_obj_file)
            # 删除临时生成的OBJ文件
            # os.remove(temp_obj_file)
    else:
        print(f"未找到指定的FBX文件: {fbx_file}")