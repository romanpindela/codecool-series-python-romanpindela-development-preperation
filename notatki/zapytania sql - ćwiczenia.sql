zapytnia sql:

-- (1) pokaż aktorów w danych show 
select ac.name as "actor name", sch.*, s.title
from shows as s
inner join show_characters as sch
on s.id = sch.show_id
inner join actors as ac
on sch.actor_id = ac.id
ORDER by ac.name, sch.show_id, s.title

-- (2) pokaż aktorów w danych show z rokiem show
select ac.name as "actor name", sch.*, s.title, to_char(s.year, 'yyyy') as year
from shows as s
inner join show_characters as sch
on s.id = sch.show_id
inner join actors as ac
on sch.actor_id = ac.id
ORDER by ac.name, year, sch.show_id, s.title


-- (3) pokaż aktorów w danych show z rokiem show - game of thrones
select ac.name as "actor name", sch.character_name, s.title, to_char(s.year, 'yyyy') as year
from shows as s

inner join show_characters as sch
on s.id = sch.show_id

left join actors as ac
on sch.actor_id = ac.id

WHERE s.title = 'Game of Thrones'
ORDER by ac.name, year, sch.show_id, s.title


-- (4) pokaż aktorów w danych show z rokiem show - puste pola - postacie bez nazwy (epizodyczne)
select ac.name as "actor name", sch.character_name, sch.show_id, s.id, s.title, to_char(s.year, 'yyyy') as year
from shows as s

inner join show_characters as sch
on s.id = sch.show_id

inner join actors as ac
on sch.actor_id = ac.id


ORDER by ac.name, year, sch.show_id, s.title


-- (5) pokaż aktorów w danych show z rokiem show - i numerem sezonu
select ac.name as "actor name", sch.character_name, sch.show_id, 
s.id, s.title, to_char(s.year, 'yyyy') as year, 
se.title as "season number"

from shows as s

inner join show_characters as sch
on s.id = sch.show_id

inner join actors as ac
on sch.actor_id = ac.id

inner join seasons as se
on s.id = se.show_id

ORDER by ac.name,  s.title, se.title, year, sch.show_id
