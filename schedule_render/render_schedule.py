from geom import geom
from vector import vector

from schedule_funcs import schedule_funcs


schedule_tasks=schedule_funcs.schedule_tasks
task_class=schedule_funcs.task_class
convert_to_external=schedule_funcs.convert_to_external

def build_table(events,fn="test_calendar"):
    
    #events=[(0,9,11,"hello there"),(2,17,18,"tea")]
    #I could use some calendar negotiation, but that's probably
    #more advanced and would fit better somewhere else.
    
    #let's just build a grid?
    out_o=[]
    d=0
    m=7
    
    x_size=0.6
    y_size=0.4
    
    hour_spacing=0.6
    event_spacing=0
    day_spacing=x_size+0.3#hour_spacing
    
    
    
    while d < m:
        h=0
        hm=24
        # ok so the hour looping is wrong,
        # i need to loop over the events
        # and draw from there.
        
        #wait this is drawing the grid.
        while h<hm:
            #hour_spacing*(duration)+event_spacing*(duration)
            position=vector.Vector(d*day_spacing,h*hour_spacing,0)
            if d==0:
                out_o.append(geom.Text(local_position=position-vector.Vector(0.5,0,0),text=str(h)))
            offset=vector.Vector(0.05,0.05,0)
            out_o.append(geom.rectangle(d_vec=vector.Vector(x_size,y_size,0),
                local_position=position))
            
            h+=1
        
        h=0
        for event in events:
            if d==event[0]:
                h=event[1]
                duration=event[2]-event[1]-1
                
                if h+duration<24:
                    #if it fits on the table
                    position=vector.Vector(d*day_spacing,h*hour_spacing,0)
                    tp=position.copy()
                    tp.x+=x_size*0.5
                    out_o.append(
                    geom.rectangle(local_position=position-offset,
                    d_vec=vector.Vector(x_size+0.1,y_size+0.1+hour_spacing*duration,0))
                    )
                    print("scheduling",event[3].name,"at",d,h)
                    out_o.append(geom.Text(local_position=tp,text=event[3].name[:6]))
                else:
                    this_day=23-h
                    overlap=(h+duration)-23
                    
                    #same day
                    position=vector.Vector(d*day_spacing,h*hour_spacing,0)
                    tp=position.copy()
                    tp.x+=x_size*0.5
                    out_o.append(
                    geom.rectangle(local_position=position-offset,
                    d_vec=vector.Vector(x_size+0.1,y_size+0.1+hour_spacing*this_day,0))
                    )
                    
                    out_o.append(geom.Text(local_position=tp,text=event[3].name[:6]))
                    
                    if True:
                        #next day
                        if d+1<7:
                            position=vector.Vector((d+1)*day_spacing,0,0)
                        else:
                            #loop around the week
                            position=vector.Vector((0)*day_spacing,0,0)
                            
                        tp=position.copy()
                        tp.x+=x_size*0.5
                        out_o.append(
                        geom.rectangle(local_position=position-offset,
                        d_vec=vector.Vector(x_size+0.1,y_size+0.1+hour_spacing*overlap,0))
                        )
                        #print("scheduling",event[3].name,"at",d,h)
                        out_o.append(geom.Text(local_position=tp,text=event[3].name[:6]))
                        
                    
        d+=1
    view_box_d=geom.make_view_box_d(out_o,scale=1.1)
    final_l=[]
    for x in out_o:
        final_l.append(x.as_svg())
        
        
    geom.main_svg(final_l,fn+".svg",view_box_d=view_box_d)
    


    
def test():
    tasks=[task_class("vaccuum",0.5,4,priority=2),
            task_class("wake up, wash, coffee",1,0,priority=0),
            task_class("work session",3,prefered_time=9,prefered_day_type="work",priority=0),
            task_class("work session2",3,prefered_time=14,prefered_day_type="work",priority=0),
            task_class("clear kitchen",0.5,7,priority=2),
            task_class("groceries",1,prefered_day_frequency=1,priority=2),
            task_class("cooking and eating",1,prefered_time=12,priority=1),
            task_class("schedule review",0.5,7,prefered_time=9,priority=2),
            task_class("sleep",9,prefered_time=22,prefered_day_frequency=0,priority=0),
            ]
    schedule=schedule_tasks(tasks)
    build_table(schedule,"regular")
    
    schedule=convert_to_external(schedule)
    build_table(schedule,"blocked")

if __name__=="__main__":
    test()
    
