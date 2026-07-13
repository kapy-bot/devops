import { useEffect, useState } from "react";

import { createTodo, deleteTodo, listTodos, updateTodo } from "./api";

export default function App() {
  const [todos, setTodos] = useState([]);
  const [title, setTitle] = useState("");
  const [error, setError] = useState(null);

  const refresh = () => listTodos().then(setTodos).catch(setError);

  useEffect(() => {
    refresh();
  }, []);

  const handleAdd = async (e) => {
    e.preventDefault();
    if (!title.trim()) return;
    await createTodo({ title });
    setTitle("");
    refresh();
  };

  const handleToggle = async (todo) => {
    await updateTodo(todo.id, { completed: !todo.completed });
    refresh();
  };

  const handleDelete = async (id) => {
    await deleteTodo(id);
    refresh();
  };

  return (
    <main style={{ maxWidth: 480, margin: "2rem auto", fontFamily: "sans-serif" }}>
      <h1>Todo</h1>
      {error && <p style={{ color: "red" }}>{error.message}</p>}
      <form onSubmit={handleAdd} style={{ display: "flex", gap: 8 }}>
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="What needs doing?"
          style={{ flex: 1 }}
        />
        <button type="submit">Add</button>
      </form>
      <ul style={{ listStyle: "none", padding: 0 }}>
        {todos.map((todo) => (
          <li key={todo.id} style={{ display: "flex", gap: 8, alignItems: "center" }}>
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={() => handleToggle(todo)}
            />
            <span style={{ textDecoration: todo.completed ? "line-through" : "none", flex: 1 }}>
              {todo.title}
            </span>
            <button onClick={() => handleDelete(todo.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </main>
  );
}
