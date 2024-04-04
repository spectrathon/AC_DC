'use client'
import { config } from "@/config"
import { useEffect, useState } from "react"



export default function Page({ params }: { params: { code: string } }) {
    const [courseData, setCourseData] = useState<{ name: string, topics: Array<string>, code: string } | null>(null)

    useEffect(() => {
        fetch(`${config.server}/CreateMCQ?` + new URLSearchParams({
            query: params.code
        })).then(resp => resp.json())
            .then(d => setCourseData(d))
    }, [])
    if (courseData === null) {
        return <div>Loading ..</div>
    }
    return <div className="">
        <h1 className="text-xl border-b p-4">{courseData.name}</h1>
        <h3>Topics</h3>
        <div>
            {courseData.topics.map(d => <div>{d}</div>)}
        </div>
    </div>
}