export interface RegisterPayload {
  login: string;
  password: string;
}

export async function registerUser(data: RegisterPayload): Promise<string> {
  const response = await fetch("/api/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (response.ok) {
    return "user создан";
  }

  // Специфические ошибки
  if (response.status === 409) {
    const err = await response.json().catch(() => null);
    throw new Error(err?.detail ?? "Логин уже существует");
  }

  if (response.status === 422) {
    const err = await response.json().catch(() => null);
    const detail = err?.detail?.[0]?.msg ?? "Ошибка валидации";
    throw new Error(detail);
  }

  // Любая другая ошибка
  let message = "Неизвестная ошибка";
  const contentType = response.headers.get("Content-Type");

  if (contentType?.includes("application/json")) {
    const err = await response.json().catch(() => null);
    message = err?.detail ?? JSON.stringify(err) ?? message;
  } else {
    const text = await response.text().catch(() => null);
    if (text) message = text;
  }

  console.error("Ошибка при регистрации:", response.status, message);
  throw new Error(message);
}


export function validateLogin(login: string): string | null {
  const pattern = /^[A-Za-z0-9._-]{3,32}$/;
  if (!pattern.test(login)) {
    return "login должен быть 3–32 символа, латиница/цифры/._-";
  }
  return null;
}

export function validatePassword(password: string): string | null {
  if (password.length < 8) {
    return "пароль должен быть минимум 8 символов";
  }
  if (!/[A-Z]/.test(password)) {
    return "пароль должен содержать минимум одну заглавную букву";
  }
  if (!/[a-z]/.test(password)) {
    return "пароль должен содержать минимум одну строчную букву";
  }
  if (!/[0-9]/.test(password)) {
    return "пароль должен содержать минимум одну цифру";
  }
  if (!/[!@#$%^&*()_\-+=\[\]{};:'",.<>/?\\|`~]/.test(password)) {
    return "пароль должен содержать минимум один спецсимвол";
  }
  return null;
}

