import { useState } from "react";
import "../styles/register.css";
import { registerUser } from "../api";
import { validateLogin, validatePassword } from "../api";

export default function Register() {
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    // Клиентская валидация
    const loginErr = validateLogin(login);
    if (loginErr) return setError(loginErr);

    const passErr = validatePassword(password);
    if (passErr) return setError(passErr);

    try {
      setLoading(true);
      const message = await registerUser({ login, password });
      setSuccess(message);
      setLogin("");
      setPassword("");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-container">
      <h1>Регистрация</h1>

      <form onSubmit={handleSubmit} className="register-form">
        <label>
          Логин:
          <input
            type="text"
            value={login}
            onChange={(e) => setLogin(e.target.value)}
            placeholder="Введите логин"
          />
        </label>

        <label>
          Пароль:
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Введите пароль"
          />
        </label>

        <button type="submit" disabled={loading}>
          {loading ? "Отправка..." : "Зарегистрироваться"}
        </button>
      </form>

      {error && <div className="error-box">{error}</div>}
      {success && <div className="success-box">{success}</div>}
    </div>
  );
}
