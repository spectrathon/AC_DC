import { Session } from "inspector";
import { NextAuthOptions } from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import GoogleProvider from "next-auth/providers/google";
// import { auth, db } from "@/firebase";
// import { doc, getDoc } from "firebase/firestore";


export const authOptions: NextAuthOptions = {
  providers: [
    // CredentialsProvider({
    //   name: "Credentials",
    //   credentials: {
    //     username: {
    //       label: "Username: ",
    //       type: "text",
    //       placeholder: "Username",
    //     },
    //     password: {
    //       label: "Password: ",
    //       type: "password",
    //     },
    //   },
    //   async authorize(credentials) {
    //     const user = {
    //       id: "10",
    //       name: "AXON",
    //       password: "ABCDE",
    //     };
    //     if (
    //       credentials?.username === user.name &&
    //       credentials?.password === user.password
    //     ) {
    //       return user;
    //     }
    //     return null;
    //   },
    // }),
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID as string,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET as string
    })
  ],
  // callbacks: {
  //   async session({ session, user, token }:any) {
  //     if(session.user){
  //       const userRef = doc(db, "Users", String(session.user?.email));
  //       // console.log(token)
  //       const docSnap = await getDoc(userRef);
  //        if (docSnap.exists()) {
  //         session.user.name=docSnap.data().Name;
  //         session.user.group=docSnap.data().Group;
  //       }
        
  //     }
  //     return session
  //   },
  
  // },
  pages: {
    signIn: "/api/signin",
  },
};


