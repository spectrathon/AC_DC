'use client'
import { useState, useEffect } from "react";
import { db } from "@/app/firebase/confing";
import { FaTrophy } from "react-icons/fa";
import {
  collection,
  query,
  orderBy,
  getDocs,
  where,
  addDoc,
} from "firebase/firestore";
import { useSession } from "next-auth/react";

interface User {
  username: string;
  email: string;
  level: number;
}

export default function Home() {
  const [userData, setUserData] = useState<User[]>([]);
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


  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const usersRef = collection(db, "users");
        const q = query(usersRef, orderBy("level", "desc"));
        const querySnapshot = await getDocs(q);
        const userDataMap: Record<string, User> = {};

        querySnapshot.forEach((doc) => {
          const data = doc.data() as User;
          // Group users by email and keep only the highest level for each email
          if (!userDataMap[data.username] || userDataMap[data.username].level < data.level) {
            userDataMap[data.username] = data;
          }
        });

        const uniqueUserData = Object.values(userDataMap);
        setUserData(uniqueUserData);
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    };

    fetchUserData();
  }, []); // Empty dependency array ensures this effect runs only once on page load

  const [searchQuery, setSearchQuery] = useState<string>("");
  const [isFetching, setIsFetching] = useState(false);
  const [courses, setCourses] = useState<
    Array<{
      name: string;
      code: string;
    }> | false
  >([]);

  const search = () => {
    setIsFetching(true);
    fetch(`${config.server}/search?` + new URLSearchParams({
      query: searchQuery
    }))
      .then((resp) => resp.json())
      .then((d) => {
        setCourses(d.courses);
        console.log(d);
        setIsFetching(false);
      });
  };

  return (
    <main>
      <div className=" flex p-9 text-4xl gap-4 ">
        <p className=" flex text-4xl text-yellow-400 ">Leaderboard </p><FaTrophy className="text-yellow-400" />
      </div>
      {/* Display user data */}
      <div className=" px-10 flex flex-col gap-8">
      {userData.map((user, index) => (
        <div className=" bg-slate-600 rounded-2xl flex justify-between" key={index}>
          <a className=" p-4">{user.email}</a>
          <a className=" p-4">{user.level}</a>
        </div>
      ))}
      </div>
    </main>
  );
}
