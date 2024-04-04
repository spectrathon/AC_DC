'use client'

import { useEffect, useState } from "react";

import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion"
import { Button } from "@/components/ui/button";
import Link from "next/link";
import useGameStore from "@/components/state";
import { useRouter } from "next/navigation";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { config } from "@/config";




export default function Home() {
  const router = useRouter()
  const [searchCourse, setSearchCourse] = useState<string | null>(null)
  const [currentCourse, setCurrentCourse] = useState<string | null>(null)
  const [searchQuery, setSearchQuery] = useState<string>("")
  const [isFetching, setIsFetching] = useState(false)
  const [isPresent, setIsPresent] = useState(0)
  const [file, setFile] = useState<File | null>(null)
  const [courses, setCourses] = useState<Array<{
    name: string,
    code: string
  }> | false>([])
  const { playerLives } = useGameStore()
  const getCourses = () => {
    const fd = new FormData()

    if (file !== null) {
      fd.append('file', file)

    }
    setIsFetching(true)
    fetch(`${config.server}/search?` + new URLSearchParams({
      query: searchQuery
    })
      , {
        method: "POST",
        body: fd
      })
      .then(resp => resp.json())
      .then(d => {
        setIsPresent(d.present)
        setCourses(d.courses)
        console.log(d)
        setIsFetching(false)
      })

  }
  return (
    <main className="p-8 ">
      <div>
        <Label className="text-2xl mb-6">Choose Course</Label>
        <div className="flex gap-2 mt-2">
          <Input className="h-16 mb-2" value={searchQuery as string} onChange={(e) => setSearchQuery(e.target.value)} />
          <Input className="h-16 mb-2" type="file" accept=".txt" onChange={(e) => setFile(e.target.files && e.target.files[0] as File)} />

        </div>
        <div className=" flex flex-wrap gap-1">
          {courses && courses.map(i => <Button type="button" className="block " onClick={() => setCurrentCourse(i.name)}>{i.name}</Button>)}
        </div>
        <Button disabled={(playerLives === 0)&&(file===null)} onClick={() => currentCourse === null ? getCourses() : router.push(`/Quiz/${currentCourse}`)} className="w-full py-3 bg-orange-400  h-16 text-lg p-4 rounded-md hover:bg-orange-300  mt-4 ">
          {currentCourse === null ? "Search" : `Start ${currentCourse} Quiz`}
        </Button>
      </div>
    </main>
  );
}
