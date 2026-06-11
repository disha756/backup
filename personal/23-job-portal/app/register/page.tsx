"use client";

// import { useState } from "react";
import styles from "../styles/register.module.css";
import { registerUser } from "../services/auth";

export default function RegisterPage() {
  //   const [name, setName] = useState("");
  //   const [email, setEmail] = useState("");
  //   const [password, setPassword] = useState("");
  //   const [message, setMessage] = useState("");

  //   async function handleSubmit(e: React.FormEvent) {
  //     e.preventDefault();

  //     try {
  //       const data = await registerUser(name, email, password);

  //       setMessage(data.message);

  //       setName("");
  //       setEmail("");
  //       setPassword("");
  //     } catch (error: any) {
  //       console.log(error);
  //       setMessage(error.message);
  //     }
  //   }

  return (
    <main className={styles.register}>
      <form className={styles.form} action={registerUser}>
        <label htmlFor="name">Name</label>
        <input
          // value={name}
          name="name"
          // onChange={(e) => setName(e.target.value)}
          placeholder="Name"
        />

        <label htmlFor="email">Email address</label>
        <input
          // value={email}
          name="email"
          // onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
        />

        <label htmlFor="password">Password</label>
        <input
          type="password"
          // value={password}
          name="password"
          // onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
        />

        <button type="submit">Register</button>

        {/* <p>{message}</p> */}
      </form>
    </main>
  );
}
