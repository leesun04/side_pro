import streamlit as st

def todo_list_page():
    st.title("✅ 나의 할 일 (Todo List)")
    st.subheader("오늘의 운동 목표를 관리해보세요.")

    # Initialize session state for todos if it doesn't exist
    if 'todos' not in st.session_state:
        st.session_state.todos = [
            {"task": "오늘의 운동 계획 세우기", "done": True},
            {"task": "스트레칭 10분", "done": True},
            {"task": "스쿼트 3세트", "done": False},
        ]

    # --- Input form to add new todos ---
    with st.form("new_todo_form", clear_on_submit=True):
        new_todo = st.text_input("새로운 할 일 추가:", placeholder="예: 런닝머신 30분")
        submitted = st.form_submit_button("추가")
        if submitted and new_todo:
            st.session_state.todos.append({"task": new_todo, "done": False})
            st.rerun()

    st.markdown("---")

    # --- Display Todos ---
    st.header("해야 할 일")
    
    active_todos = [todo for todo in st.session_state.todos if not todo["done"]]
    if not active_todos:
        st.success("모든 할 일을 완료했습니다! 🎉")

    for i, todo in enumerate(st.session_state.todos):
        if not todo["done"]:
            # Use a unique key for each checkbox
            is_done = st.checkbox(todo["task"], key=f"todo_{i}")
            if is_done:
                # Update the 'done' status in the original list
                st.session_state.todos[i]["done"] = True
                st.rerun()

    # --- Display Completed Todos in an Expander ---
    st.markdown("---")
    with st.expander("완료된 일 보기"):
        completed_tasks = [todo for todo in st.session_state.todos if todo["done"]]
        if not completed_tasks:
            st.write("아직 완료된 일이 없습니다.")
        else:
            for todo in completed_tasks:
                # Using a disabled checkbox to show the completed state
                st.checkbox(f"~~{todo['task']}~~", value=True, disabled=True)

    # --- Button to clear completed tasks ---
    if st.button("완료된 일 모두 지우기"):
        # Filter out the completed tasks
        st.session_state.todos = [todo for todo in st.session_state.todos if not todo["done"]]
        st.rerun()


if __name__ == "__main__":
    # To make the page runnable independently
    st.set_page_config(page_title="Todo App", page_icon="✅")
    todo_list_page()