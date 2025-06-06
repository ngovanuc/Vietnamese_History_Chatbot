import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { MessageSquare, ChevronRight } from "lucide-react";

export default function FollowUpSuggestions() {
  const [selectedIndex, setSelectedIndex] = useState(null);
  
  // Default suggestions if none provided in props
  const suggestions = props.suggestions || [
    { "label": "Tell me more", "content": "Explain this in more detail." },
    { "label": "Explain it simply", "content": "Explain this in simple terms." },
    { "label": "Code example", "content": "Give me a code example." }
  ];
  
  const handleSuggestionClick = (suggestion, index) => {
    setSelectedIndex(index);
    // Send the suggestion's content as a user message
    sendUserMessage(suggestion.content);
  };
  
  return (
    <Card className="w-full max-w-md border-2 border-primary/10">
      <CardHeader className="pb-2">
        <CardTitle className="text-md font-medium flex items-center gap-2">
          <MessageSquare className="h-4 w-4" />
          {props.title || "Các chủ đề có thể bạn sẽ quan tâm...🤔"}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex flex-col gap-2">
          {suggestions.map((suggestion, index) => (
            <button key={index} onClick={() => handleSuggestionClick(suggestion, index)} className="flex items-center justify-between w-full p-2 bg-white rounded hover:bg-gray-100">
              <span>{suggestion.label}</span>
              <ChevronRight className="h-4 w-4 ml-2 opacity-70" />
            </button>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}