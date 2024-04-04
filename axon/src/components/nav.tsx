'use client'
import { IoHome } from "react-icons/io5";
import { FaSearch } from "react-icons/fa";
import { FaTrophy } from "react-icons/fa";
import { FaUserCircle } from "react-icons/fa";
import Link from "next/link";
import { usePathname } from "next/navigation";



export default function Nav() {
    const path = usePathname()
    return <>
        <div className="w-full  bg-black-100 flex justify-evenly fixed bottom-0  border-t  border-white/10">
            <Link className={` ${path === "/" ? "bg-orange-700/20" : "text-white/40 hover:text-white hover:bg-slate-100/10"}   transition-colors  p-10 text-lg w-full items-center justify-center flex`} href={'/'}><IoHome /></Link>
            <Link className={` ${path === "/Leaderboard" ? "bg-orange-700/20" : "text-white/40 hover:text-white hover:bg-slate-100/10"}   transition-colors  p-10 text-lg w-full items-center justify-center flex`} href={'/Leaderboard'}><FaTrophy /></Link>
            <Link className={` ${path === "/Profile" ? "bg-orange-700/20" : "text-white/40 hover:text-white hover:bg-slate-100/10"}   transition-colors  p-10 text-lg w-full items-center justify-center flex`} href={'/Profile'}><FaUserCircle /></Link>
        </div>
    </>
}