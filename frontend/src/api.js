const BASE_URL = "/api";

async function request(path, options) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    throw new Error(`Request failed: ${res.status}`);
  }
  if (res.status === 204) return null;
  return res.json();
}

export const listTodos = () => request("/todos");

export const createTodo = (todo) =>
  request("/todos", { method: "POST", body: JSON.stringify(todo) });

export const updateTodo = (id, changes) =>
  request(`/todos/${id}`, { method: "PATCH", body: JSON.stringify(changes) });

export const deleteTodo = (id) =>
  request(`/todos/${id}`, { method: "DELETE" });

export const clearCompleted = () =>
  request("/todos/completed", { method: "DELETE" });
