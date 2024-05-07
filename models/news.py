class News:
    def __init__(self, title, content, age, link, media_img, media_video, locality, category=None):
        self.title = title
        self.content = content
        self.age = age
        self.link = link
        self.media_img = media_img
        self.media_video = media_video
        self.locality = locality
        self.category = category

    def __str__(self):
        return f"Título: {self.title}\nConteúdo: {self.content}\nIdade: {self.age}\nLink: {self.link}\nMídia de Imagem: {self.media_img}\nMídia de Vídeo: {self.media_video}\nCategoria: {self.category}\n"

    def to_dict(self):
        return {
            'title': self.title,
            'content': self.content,
            'age': self.age,
            'link': self.link,
            'media_img': self.media_img,
            'media_video': self.media_video,
            'locality': self.locality,
            'category': self.category
        }
