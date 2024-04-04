import { config } from "@/config";
import Link from "next/link";



export default function CourseCard(params: { courseName: string, courseCode: string }) {
    return <Link className="block w-full  hover:underline  " href={`/Course/${params.courseCode}`}>{params.courseName}</Link>
}