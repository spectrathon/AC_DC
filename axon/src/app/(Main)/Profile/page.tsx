'use client'
import { useState, useEffect } from 'react';
import { useSession } from 'next-auth/react';
import { GoDotFill } from "react-icons/go";
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { signOut } from "next-auth/react";
import { db } from '@/app/firebase/confing';
import { collection, addDoc, setDoc, doc, query, where, getDocs } from 'firebase/firestore';

export default function Home() {
  const { data: session } = useSession();
  const [status, setStatus] = useState<boolean>(false);
  const [name, setName] = useState<any>(null); // Initialize as null
  const [email, setEmail] = useState<any>(null); // Initialize as null
  const [image, setImage] = useState<any>(null); // Initialize as null
  const [level, setLevel] = useState<number | null>(null); // Initialize as null for user level
  const [achievements, setAchievements] = useState<any[]>([]); // State to store achievements

  useEffect(() => {
    const fetchData = async () => {
      if (session && session.user && !status) {
        const { name, email, image } = session.user;
        setName(name);
        setEmail(email);
        setImage(image);
        setStatus(false);
        
        const checkUserExistsInDatabase = async () => {
          try {
            const usersRef = collection(db, 'users');
            const q = query(usersRef, where('email', '==', email));
            const querySnapshot = await getDocs(q);
            return !querySnapshot.empty;
          } catch (error) {
            console.error('Error checking user existence:', error);
            return false;
          }
        };
    
        const addUserToDatabase = async () => {
          try {
            await addDoc(collection(db, "users"), {
              username: name,
              email: email,
              img: image,
              level: 0, // Set default level here if needed
              course: [{ course_id: "", course_name: "", course_progress: 0 }],
              friend: [{ friend_id: "" }],
              achievement: [
                { achievement_id: "01", achievement_name: "super 5", achievement_description: "solve first 5 questions", achievement_status: false, achievement_img: "https://i.ibb.co/Ny2f9pF/GEC-spectrum-ppt-removebg-preview.png" },
                { achievement_id: "02", achievement_name: "super 10", achievement_description: "solve first 10 questions", achievement_status: false, achievement_img: "https://i.ibb.co/tDFnc5m/GEC-spectrum-ppt-2-removebg-preview.png"  },
                { achievement_id: "03", achievement_name: "super 15", achievement_description: "solve first 15 questions", achievement_status: false, achievement_img: "https://i.ibb.co/9TbrqZ2/GEC-spectrum-ppt-1-removebg-preview.png" }
              ]
            });
            console.log("User data added to the database.");
          } catch (error) {
            console.error("Error adding user data to the database: ", error);
          }
        };
    
        const getUserLevel = async () => {
          try {
            const usersRef = collection(db, 'users');
            const q = query(usersRef, where('email', '==', email));
            const querySnapshot = await getDocs(q);
            if (!querySnapshot.empty) {
              querySnapshot.forEach((doc) => {
                const userData = doc.data();
                setLevel(userData.level); // Set the user's level from the database
              });
            }
          } catch (error) {
            console.error('Error fetching user level:', error);
          }
        };

        const getUserAchievements = async () => {
          try {
            const usersRef = collection(db, 'users');
            const q = query(usersRef, where('email', '==', email));
            const querySnapshot = await getDocs(q);
            if (!querySnapshot.empty) {
              querySnapshot.forEach((doc) => {
                const userData = doc.data();
                setAchievements(userData.achievement.filter((ach: any) => ach.achievement_status));
              });
            }
          } catch (error) {
            console.error('Error fetching user achievements:', error);
          }
        };

        const userDataExists = await checkUserExistsInDatabase();
        if (!userDataExists) {
          await addUserToDatabase();
        } else {
          await getUserLevel(); // Fetch user's level if user exists
          await getUserAchievements(); // Fetch user's achievements if user exists
        }
      }
    };

    fetchData();
  }, [session, status]);

  return (
    <main>
      <div className='flex flex-row-reverse justify-between'>
        <p className="block px-4 py-2 text-white-800 cursor-pointer" onClick={() => signOut({ callbackUrl: 'http://localhost:3000/' })}>Log out</p>
        {status && (
          <div className="">
            <GoDotFill className='size-10 text-lime-500' />
          </div>
        )}
      </div>
      <div className="flex flex-col justify-center">
        <div className="flex flex-col justify-center items-center p-10 gap-5">
          <Avatar className="w-40 h-40 border-solid border-white border-4">
            <AvatarImage src={session && session.user && session.user.image} />
            <AvatarFallback>CN</AvatarFallback>
          </Avatar>
          <p>{session && session.user && session.user.name}</p>
        </div>

        <div className='flex flex-col px-10 gap-10'>
          <h3 className='m-0'>Level: {level}</h3> {/* Display user's level */}
        
          <div>
            <h3>Achievements:</h3>
            <div className="flex gap-2">
              {achievements.map((achievement: any) => (
                <div key={achievement.achievement_id}>
                  <img className=' w-12 h-12' src={achievement.achievement_img} alt={achievement.achievement_name} />
                </div>
              ))}
            </div>
          </div>

          <div>
            <h3>courses:</h3>
          </div>
        </div>
      </div>
    </main>
  );
}