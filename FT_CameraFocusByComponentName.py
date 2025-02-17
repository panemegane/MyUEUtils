import unreal
import sys

args = sys.argv

def focus_on_component(component_name):

    unreal.log(f"{component_name} にフォーカスします。")
    world = unreal.UnrealEditorSubsystem().get_game_world()
    if(world == None): # 非PIE時
        # Editor Actor Subsystem を取得
        editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

        # 現在のレベルにあるすべてのアクターを取得
        all_actors = editor_actor_subsystem.get_all_level_actors()
    else: # PIE時
        unreal.log(f"World: {world.get_name()}")
        all_actors = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Actor)


    # 指定されたコンポーネントを持つアクターを検索
    target_component = None
    for actor in all_actors:
        # unreal.log(actor.get_name())
        # アクターのすべてのコンポーネントを取得
        components = actor.get_components_by_class(unreal.SceneComponent)
        for component in components:
            if component.get_name() == component_name:
                target_component = component
                break
        if target_component:
            break

    if not target_component:
        unreal.log_error(f"コンポーネント '{component_name}' が見つかりませんでした。")
        return

    # ターゲットコンポーネントのワールド位置を取得
    target_location = target_component.get_world_location()

    # Editor Scripting Subsystem を取得
    editor_scripting_subsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)

    # 現在のカメラ位置と回転を取得
    camera_location, camera_rotation = editor_scripting_subsystem.get_level_viewport_camera_info()

    # ビューポートをターゲットにフォーカス
    editor_scripting_subsystem.set_level_viewport_camera_info(target_location, camera_rotation)
    unreal.log(f"視点をコンポーネント '{component_name}' にフォーカスしました。")

# 実行例: "MyUniqTrigger" という名前のコンポーネントにフォーカス
focus_on_component(args[1])
