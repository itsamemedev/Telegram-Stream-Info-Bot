# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
  9557  GET              /                                                dashboard
 11449  GET              /api/abo/status                                  api_abo_status
 11403  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 10345  GET              /api/automation/status                           api_automation_status
 10367  POST             /api/automation/toggle                           api_automation_toggle
 17785  GET              /api/channel/categories                          api_channel_categories
 17791  POST             /api/channel/set                                 api_channel_set
 17638  GET              /api/channels/status                             api_channels_status
 17312  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 17295  GET              /api/clips                                       api_clips
 17341  POST/DELETE      /api/clips/clear                                 api_clips_clear
 17220  GET              /api/debug/threads                               api_debug_threads
 11414  GET              /api/events                                      api_events
 10986  GET              /api/events/stream                               api_events_stream
 10813  GET              /api/health                                      api_health
 17254  POST             /api/highlights/config                           api_highlights_config
  9491  POST             /api/login                                       dashboard_login_submit
 11742  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 10901  GET              /api/notify/status                               api_notify_status
 10912  POST             /api/notify/test                                 api_notify_test
 11503  GET              /api/proxy/heatmap                               api_proxy_heatmap
 11480  GET              /api/proxy/trend                                 api_proxy_trend
 17361  GET              /api/tts/<fn>                                    api_tts_file
 18087  GET              /api/upload_window                               api_upload_window
 11103  GET              /archive/<int:eid>/download                      archive_download
 11131  GET              /download/<int:recording_id>                     download
 11060  GET              /health                                          health
 17189  GET              /healthz                                         healthz
  9482  GET              /login                                           dashboard_login_page
  9512  GET              /logout                                          dashboard_logout
  9519  GET              /manifest.webmanifest                            pwa_manifest
 18060  GET              /overlay                                         overlay_page
  9543  GET              /pwa-icon-<variant>.png                          pwa_icon
  9529  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (327)

```
   182  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   394  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
   195  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   165  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
  1003  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   743  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   874  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   854  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   892  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   816  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   356  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   367  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   377  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   400  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   407  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   418  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   551  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   649  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1241  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1273  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   340  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   956  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   936  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1109  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1157  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1208  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1067  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   911  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   389  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   653  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   535  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   518  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   510  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   346  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   362  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   697  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   662  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   682  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   569  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    49  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    78  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
   216  GET/POST         /api/auto-archive-rules                          api_archive_rules   [nc/routes/wartung.py]
   241  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete   [nc/routes/wartung.py]
   246  POST             /api/auto-archive-rules/run                      api_archive_rules_run   [nc/routes/wartung.py]
   163  GET              /api/azrael/agents                               api_azrael_agents   [nc/routes/azrael.py]
    99  POST             /api/azrael/ask                                  api_azrael_ask   [nc/routes/azrael.py]
   222  GET/POST         /api/azrael/context                              api_azrael_context   [nc/routes/azrael.py]
   120  GET              /api/azrael/core                                 api_azrael_core   [nc/routes/azrael.py]
   342  POST             /api/azrael/live_pause                           api_azrael_live_pause   [nc/routes/azrael.py]
   328  GET              /api/azrael/live_status                          api_azrael_live_status   [nc/routes/azrael.py]
   350  POST             /api/azrael/live_test                            api_azrael_live_test   [nc/routes/azrael.py]
   174  GET              /api/azrael/memories                             api_azrael_memories   [nc/routes/azrael.py]
   406  POST             /api/azrael/persona                              api_azrael_persona_set   [nc/routes/azrael.py]
   397  GET              /api/azrael/personas                             api_azrael_personas   [nc/routes/azrael.py]
   314  GET              /api/azrael/piper_status                         api_azrael_piper_status   [nc/routes/azrael.py]
   190  POST             /api/azrael/react                                api_azrael_react   [nc/routes/azrael.py]
   231  GET              /api/azrael/reaction                             api_azrael_reaction   [nc/routes/azrael.py]
   243  GET              /api/azrael/reactions                            api_azrael_reactions   [nc/routes/azrael.py]
   372  GET              /api/azrael/transcript                           api_azrael_transcript   [nc/routes/azrael.py]
   281  POST             /api/azrael/tts_test                             api_azrael_tts_test   [nc/routes/azrael.py]
   267  GET              /api/azrael/voices                               api_azrael_voices   [nc/routes/azrael.py]
   379  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model   [nc/routes/azrael.py]
   286  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
   208  POST             /api/backup/run                                  api_backup_run   [nc/routes/wartung.py]
   174  GET              /api/backup/status                               api_backup_status   [nc/routes/wartung.py]
   157  POST             /api/backup/system                               api_backup_system   [nc/routes/wartung.py]
   371  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
   348  GET              /api/bookmarks                                   api_bookmarks_list   [nc/routes/auskunft.py]
   198  GET              /api/brain                                       api_brain   [nc/routes/brain.py]
   131  GET              /api/brain/alarms                                api_brain_alarms   [nc/routes/brain.py]
   116  GET              /api/brain/creator                               api_brain_creator   [nc/routes/brain.py]
    93  GET              /api/brain/graph                                 api_brain_graph   [nc/routes/brain.py]
   158  GET              /api/brain/growth                                api_brain_growth   [nc/routes/brain.py]
    80  GET              /api/brain/health                                api_brain_health   [nc/routes/brain.py]
    81  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    53  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
   161  GET              /api/checks                                      api_checks   [nc/routes/auskunft.py]
    40  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    52  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    52  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    87  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   122  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   415  GET              /api/community/stats                             api_community_stats   [nc/routes/auskunft.py]
   329  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   314  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   237  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
   193  POST             /api/cookies/fetch                               api_cookies_fetch   [nc/routes/settings.py]
    71  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    78  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   469  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   258  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   285  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   245  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
   164  GET              /api/defense/attacks                             api_defense_attacks   [nc/routes/abwehr.py]
   125  GET              /api/defense/crowdsec                            api_defense_crowdsec   [nc/routes/abwehr.py]
   146  GET              /api/defense/fail2ban                            api_defense_fail2ban   [nc/routes/abwehr.py]
    91  GET              /api/defense/overview                            api_defense_overview   [nc/routes/abwehr.py]
   244  POST             /api/discord/announce                            api_discord_announce   [nc/routes/discord.py]
   170  GET              /api/discord/clips_week                          api_discord_clips_week   [nc/routes/discord.py]
   188  GET              /api/discord/community                           api_discord_community   [nc/routes/discord.py]
   160  GET              /api/discord/invite                              api_discord_invite   [nc/routes/discord.py]
    63  GET              /api/discord/overview                            api_discord_overview   [nc/routes/discord.py]
   136  POST             /api/discord/webhook_test                        api_discord_webhook_test   [nc/routes/discord.py]
    79  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
   112  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   120  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    60  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   136  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
   194  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   179  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    90  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
   112  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   133  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
   150  POST             /api/evolution/proposals/bulk                    api_evolution_bulk   [nc/routes/evolution.py]
    80  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   209  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    44  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   200  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   220  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   247  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
   366  GET              /api/forecast/storage                            api_forecast_storage   [nc/routes/auskunft.py]
   284  GET              /api/freeai/status                               api_freeai_status   [nc/routes/auskunft.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   386  GET              /api/heatmap/lives/<username>                    api_heatmap_lives   [nc/routes/auskunft.py]
   381  GET              /api/heatmap/recordings                          api_heatmap_recordings   [nc/routes/auskunft.py]
   457  GET              /api/highlights                                  api_highlights   [nc/routes/auskunft.py]
    64  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    53  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   307  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    77  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   168  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    43  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   150  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   125  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   189  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    76  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    99  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   223  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   222  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   244  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
   103  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   171  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   149  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    85  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   128  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   178  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
   119  POST             /api/kickmod/config                              api_kickmod_config   [nc/routes/kickmod.py]
   167  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords   [nc/routes/kickmod.py]
   184  GET              /api/kickmod/learned                             api_kickmod_learned   [nc/routes/kickmod.py]
   215  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear   [nc/routes/kickmod.py]
   191  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote   [nc/routes/kickmod.py]
   251  POST             /api/kickmod/say                                 api_kickmod_say   [nc/routes/kickmod.py]
   221  POST             /api/kickmod/start                               api_kickmod_start   [nc/routes/kickmod.py]
    82  GET              /api/kickmod/status                              api_kickmod_status   [nc/routes/kickmod.py]
   235  POST             /api/kickmod/stop                                api_kickmod_stop   [nc/routes/kickmod.py]
   400  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard   [nc/routes/auskunft.py]
    78  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
   103  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
   113  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    52  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    70  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   225  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
   100  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    66  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    77  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   142  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   137  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   128  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    53  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    92  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   267  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   334  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   362  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   213  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   280  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   515  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    80  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   178  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   161  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   401  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   225  GET              /api/outcomes                                    api_outcomes   [nc/routes/auskunft.py]
   210  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   193  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
    94  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   177  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   460  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   435  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   296  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   142  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   832  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   914  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   942  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   953  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   819  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   881  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   868  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   849  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   319  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   494  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   489  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   537  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   420  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   747  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   511  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   474  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   447  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   721  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   591  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   680  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   586  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   519  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   299  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   764  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   387  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   642  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   797  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   782  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   343  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   581  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   567  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   550  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   607  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
   700  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   596  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   486  POST             /api/restream/<int:rid>/delete                   api_restream_delete   [nc/routes/restream.py]
   464  POST             /api/restream/<int:rid>/edit                     api_restream_edit   [nc/routes/restream.py]
   505  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   522  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   574  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   440  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   265  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   165  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   596  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   413  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   134  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   535  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   561  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   191  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   216  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   388  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   134  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   144  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
   370  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   360  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   395  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    65  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    86  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    52  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
   102  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   338  GET              /api/search                                      api_search   [nc/routes/auskunft.py]
    92  GET              /api/selftest                                    api_selftest   [nc/routes/selbsttest.py]
   428  GET              /api/shield/stats                                api_shield_stats   [nc/routes/auskunft.py]
   128  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   219  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   214  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   274  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   110  GET              /api/storage                                     api_storage   [nc/routes/wartung.py]
   116  POST             /api/storage/cleanup                             api_storage_cleanup   [nc/routes/wartung.py]
   448  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   340  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   370  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
   126  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   273  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    88  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   298  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   230  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   254  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   185  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   150  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   210  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    56  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
   206  GET              /api/summary/preview                             api_summary_preview   [nc/routes/auskunft.py]
    72  GET              /api/system                                      api_system   [nc/routes/systemlage.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   178  GET              /api/system/check_timing                         api_check_timing   [nc/routes/systemlage.py]
   117  GET              /api/system/config_drift                         api_config_drift   [nc/routes/systemlage.py]
   140  GET              /api/system/config_snapshot                      api_system_config_snapshot   [nc/routes/systemlage.py]
   238  GET              /api/system/preflight                            api_system_preflight   [nc/routes/systemlage.py]
   104  GET              /api/system/preflight_history                    api_system_preflight_history   [nc/routes/systemlage.py]
   370  GET              /api/system/resilience                           api_system_resilience   [nc/routes/systemlage.py]
   361  GET              /api/tags                                        api_tags_list   [nc/routes/auskunft.py]
   176  GET              /api/top                                         api_top   [nc/routes/auskunft.py]
   238  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   453  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   482  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   402  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   415  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   511  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   388  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   263  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   308  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   332  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   319  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   165  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   277  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   135  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   369  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   424  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   252  GET              /api/trend-7d                                    api_trend_7d   [nc/routes/auskunft.py]
   121  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
   100  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   132  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
   113  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   125  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    77  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
   101  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    55  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   463  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   429  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   488  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   468  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   451  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   444  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
   238  GET              /api/userstats                                   api_userstats   [nc/routes/auskunft.py]
   305  GET              /api/version                                     api_version   [nc/routes/auskunft.py]
    52  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    92  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   123  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
   107  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
   131  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback   [nc/routes/youtube.py]
   152  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget   [nc/routes/youtube.py]
   164  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout   [nc/routes/youtube.py]
    89  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect   [nc/routes/youtube.py]
   113  GET              /api/youtube/oauth/start                         api_youtube_oauth_start   [nc/routes/youtube.py]
    67  GET              /api/youtube/oauth/status                        api_youtube_oauth_status   [nc/routes/youtube.py]
   199  GET              /api/youtube/sendrate                            api_youtube_sendrate   [nc/routes/youtube.py]
   382  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
```

## Discord-Slash-Commands in discordbot.py (45)

```
   519  /ai                     
   992  /ask                    
   610  /assign_role            
   656  /ban                    
  1324  /botstats               
  1248  /clearwarns             
  1288  /clip                   
  1273  /clipoftheweek          
  1115  /clips                  
   571  /create_category        
   540  /create_channel         
   599  /create_group           
   582  /create_role            
   556  /create_voice           
   892  /daily                  
  1022  /event                  
  1065  /events                 
  1161  /follow                 
  1145  /help                   
   645  /kick                   
   874  /leaderboard            
  1101  /livenow                
  1131  /post_test              
   962  /profile                
   680  /purge                  
   860  /rank                   
  1088  /recstatus              
   621  /remove_role            
   533  /restream_status        
   632  /set_channel_perms      
   825  /setup_community        
   843  /setup_targets          
  1187  /stats                  
   445  /status                 
  1483  /streaminfo             
  1380  /sys_report             
  1356  /sys_unpause            
   667  /timeout                
  1259  /topstreamers           
   475  /track                  
   459  /tracklist              
  1176  /unfollow               
   508  /untrack                
  1209  /warn                   
  1233  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  1981  on_member_join
  1943  on_message
  1570  on_raw_reaction_add
  2016  on_ready
```

## Top-Level-Symbole in discordbot.py (9 Funktionen)

```
  2132-2194   _community_events_loop
  2234-2269   _disc_automod_check
   362-2091   _discord_run_once
   245-303    _discord_start
   306-359    _ensure_discord_invite
  2097-2129   _ensure_error_channel
  2197-2227   _error_channel_loop
   150-224    _uebernehmen
   227-230    starte
```

## Top-Level-Symbole in bot.py (462 Funktionen, 2 Klassen)

```
  2615-2616   _abo_key
  2636-2654   _abo_probe_dump
 14552-14559  _ad_allowlist
 15491-15497  _agent_for
 15500-15516  _ai_telemetry
 16005-16023  _alert
 18906-18956  _alert_monitor_loop
 19308-19370  _announce_loop
  3150-3153   _anthropic_key
  3160-3162   _anthropic_model
  9235-9238   _arg_int
  2607-2612   _as_dict
 16158-16180  _audio_tap_cmd
  9403-9414   _auth_cookie
  9370-9399   _auth_guard
  1729-1734   _auto_on
 17051-17069  _auto_restream_loop
 20270-20285  _azrael_broadcast_reply
 20170-20192  _azrael_chat_reply
 20153-20167  _azrael_chat_should_reply
 20198-20200  _azrael_gate_cfg
 15521-15535  _azrael_live_state
 17972-17986  _azrael_overlay_state
 15887-15941  _azrael_proactive_loop
 15339-15395  _azrael_reaction_to_chats
 20203-20210  _azrael_reply_all_chats
 20140-20150  _azrael_self_names
 20238-20267  _azrael_send_to
 15541-15562  _azrael_system
 19040-19043  _backup_active
 19121-19134  _backup_loop
 18845-18854  _brain_growth_loop
  9736-9763   _brain_growth_snapshot
  2543-2563   _brain_hint_delay
  5828-5856   _brain_notify
 10965-10982  _browser_push
  5872-5959   _build_daily_summary
 12954-12958  _build_restream_cmd
  4650-4677   _can_stop_tracking
  1842-1864   _capture_set_cookies
 11557-11560  _cfg_get
 11563-11565  _cfg_set
 17746-17781  _channel_set_all
 12096-12099  _chat_connected
 12102-12118  _chat_disconnected
  7954-7965   _chat_is_forum
 12138-12140  _chat_sanitize
 12081-12093  _chat_stat
 12121-12124  _chat_stats_snapshot
  3433-3445   _check_ai_models_sync
 10018-10061  _classify_pool_anonymity
 10064-10081  _classify_pool_anonymity_bg
   830-852    _claude_chat_sync_metered
  9264-9271   _client_ip
 19402-19429  _clip_prune
 19432-19442  _clip_recfile_for
 19804-19810  _clip_should_velocity
 19483-19565  _clip_to_discord
  3326-3335   _close_ai_session
 20316-20331  _cohost_broadcast
 20301-20302  _cohost_cfg
 20357-20369  _cohost_fire_highlight
 20305-20313  _cohost_gate
 20334-20354  _cohost_highlight
  9666-9668   _conv_messages
  6231-6292   _cookie_alarm_loop
  1933-1938   _cookie_autofetch_info
  1916-1920   _cookie_autorefresh_info
  1819-1823   _cookie_header
  1950-1983   _cookies_selbst_holen
  3639-3651   _create_index_safe
 18419-18525  _crowdsec_status
 18365-18416  _crowdsec_via_lapi
 18269-18287  _cscli_bin
 18296-18309  _cscli_path
  6121-6146   _daily_summary_loop
 18327-18344  _darf_journal_lesen
 18880-18903  _db_maintenance_loop
  6090-6118   _db_vacuum_loop
 14575-14599  _detect_foreign_ad
  1464-1475   _diag_path_owner
 15793-15837  _director_finalize
 16604-16611  _director_for
 15742-15790  _director_mark
 19717-19720  _disc_state_get
 19723-19730  _disc_state_set
 18826-18835  _discord_bot_starten
 18790-18801  _discord_einladung_merken
 18838-18842  _discord_invite
 18804-18823  _discord_kontext
 19678-19714  _discord_live_thread
 15944-15956  _discord_notify
 18762-18787  _discord_ops_alert
 19576-19674  _discord_post_user
 19373-19379  _discord_stop
  6149-6226   _disk_alarm_loop
 21746-21795  _disk_autoclean
 21798-21811  _disk_guard_loop
 11235-11237  _dump_all_threads
  9944-10007  _enrich_proxies_with_geo
  2158-2219   _ensure_cookie_file_netscape
  8013-8016   _ensure_notify_topic
 10188-10225  _ensure_proxy_ready
  7967-7994   _ensure_topic
   690-692    _env_int
   695-697    _env_int_range
 15989-16002  _event_webhook
 11911-11924  _evolution_loop
  5270-5304   _extract_file_payload
  2291-2293   _extract_urls_from_streamurl_node
 18312-18319  _f2b_sudo_hint
  4150-4160   _fehler_text
  9845-9863   _fetch_proxy_list
 16438-16466  _fetch_tiktok_room_id
   763-766    _ff_cmd
 12685-12690  _find_chromium
  3081-3083   _find_external_recorder
  2296-2298   _find_stream_urls
 11608-11633  _fire_webhooks
  7058-7067   _fork_safe
   863-876    _freeai_chat_sync_metered
 18358-18362  _geo_lookup_ips
  3314-3323   _get_ai_session
  6891-6931   _get_live_info
  2833-2840   _get_resolve_semaphore
  7291-7668   _handle_single_tracking
 21568-21570  _hb
 21573-21590  _hb_while
 12152-12154  _highlight_cfg
 12157-12186  _highlight_observe
 12693-12711  _htmlov_screenshot_cmd
 16182-16192  _httpx_proxy
 11641-11653  _in_quiet_hours
 22637-22668  _install_fast_eventloop
  9130-9184   _install_fast_json
 11240-11256  _install_faulthandler
 17097-17106  _intel_ensure_schema
 17144-17179  _intel_index_loop
 17118-17128  _intel_index_one
 17109-17115  _intel_semantic
  4639-4648   _is_authorized
  7192-7198   _is_dead
  2281-2283   _is_hevc
 18347-18349  _is_private_ip
  1628-1635   _is_process_running
  5858-5869   _is_quiet_hours
  1257-1266   _is_upload_window
  9219-9232   _json_error_handler
  6084-6085   _kick_broadcaster_id
  5996-6038   _kick_follower_count
  5980-5983   _kick_slug
 10778-10785  _kick_user_token
  3688-3691   _kind_from_filename
 11670-11675  _latest_popularity
 16819-16852  _live_react_loop
 16615-16808  _live_react_worker
 15398-15409  _live_transcript_push
 16810-16817  _live_users
 15840-15884  _living_title_loop
 19046-19118  _local_backup_scan
  9201-9215   _log_5xx
 12966-12978  _looks_like_codec_err
 12961-12963  _looks_like_source_expired
  7108-7138   _loop_fehler
 11260-11269  _loop_heartbeat
 21538-21565  _loop_lag_monitor
 11272-11340  _loop_watchdog_thread
 15278-15292  _loyalty_add
 15269-15275  _loyalty_get
 15295-15303  _loyalty_top
 11783-11785  _manual_donations_total
  4357-4376   _manual_status
  7200-7201   _mark_dead
 10464-10480  _marketing_loop
 20217-20235  _maybe_handle_command
 21897-21921  _maybe_hype_clip
  3606-3629   _migrate_columns
 20496-20507  _mod_is_exempt
 20510-20515  _mod_warn_first
 20518-20521  _mod_warn_text
 11951-11959  _modlog
  1004-1006   _multistream_targets
  7070-7071   _nc_create_subprocess_exec
  7074-7075   _nc_create_subprocess_shell
 10715-10732  _news_loop
 11978-11980  _normalize_ingest
  2474-2491   _note_check_duration
  8007-8010   _notify_topic_name
 15424-15432  _oracle_memories
 15697-15731  _oracle_memorize
 15435-15448  _oracle_persona
 15417-15421  _oracle_recent_text
 12312-12320  _ov_atomic_write
 12300-12306  _ov_bar
 14478-14490  _ov_clip_text
 12309-12310  _ov_oneline
 18024-18053  _overlay_push
 12639-12682  _overlay_render_size
 12044-12048  _overlay_session_reset
 17988-17991  _overlay_src_ok
 14562-14572  _own_invites
 12634-12636  _parse_size
 18533-18613  _parse_ssh_attacks
  6493-6526   _pause_resume_cmd
  1870-1914   _persist_refreshed_cookies
  1773-1805   _pick_checked_pull_proxy
  9300-9313   _pin_auth_value
  9359-9360   _pin_clear_fail
  9339-9342   _pin_locked
  9345-9356   _pin_note_fail
  9316-9336   _pin_ok
 17882-17907  _piper_pick_model
 17919-17966  _piper_say
 11570-11605  _post_json_threaded
 12613-12631  _probe_video_size
  1656-1673   _proc_is_recorder
 10157-10185  _proxy_pool_refresh_loop
  1739-1770   _proxy_report_recording
 11225-11227  _prune_stall_dumps
 10534-10655  _public_stats
  1941-1947   _pull_proxy_still
 15960-15986  _push_notify
  9461-9463   _pwa_dir
  9914-9929   _quick_validate_proxy
 11636-11638  _quiet_hours_config
  9426-9459   _rate_guard
 15243-15249  _react_warn
  6978-7017   _reap_proc
  2514-2536   _record_check_outcome
   758-760    _redact_stream_urls
 10084-10154  _refresh_proxy_pool
  2307-2397   _resolve_via_html
  2656-2810   _resolve_via_webcast_api_v2
  2873-2935   _resolve_via_ytdlp
 19844-19973  _resolve_youtube_ingest
 12027-12038  _restream_active_sources
 16469-16568  _restream_chat_guardian
 12189-12261  _restream_chat_push
 12286-12295  _restream_chat_push_async
 12714-12801  _restream_html_overlay_start
 12804-12817  _restream_html_overlay_stop
 11989-12012  _restream_overlay_files
 16856-16888  _restream_platform_state
 17013-17048  _restream_resume_after_restart
 12865-12923  _restream_tts_enqueue_wav
 12575-12607  _restream_tts_feeder
 12572-12573  _restream_tts_fifo_path
 12820-12847  _restream_tts_start
 12849-12863  _restream_tts_stop
 16894-17010  _restream_verify_loop
 19011-19023  _retention_loop
 19005-19008  _retention_scan
  2618-2620   _room_is_abo
  5308-5425   _run_ai_call
 11363-11376  _run_async_from_flask
 18352-18355  _run_priv
 22625-22633  _run_selfcheck_and_exit
 19026-19037  _s3_client
  7227-7278   _safe_send
  4283-4299   _sample_net_throughput
  2566-2593   _schedule_next_check
 18959-19002  _scheduler_loop
  3632-3636   _schema_pk
 11380-11385  _scraper_session
 20524-20563  _screen_full
 10829-10866  _sec_headers
  2286-2288   _select_stream_from_data_section
 22438-22622  _selfcheck
  8019-8053   _send_live_notice
  1280-1284   _should_defer_upload
 19445-19480  _shrink_for_discord
  9466-9478   _sicheres_ziel
 18857-18877  _sicherheits_erinnerung_loop
 21818-21835  _sign_health_check
 21838-21857  _sign_health_loop
  7087-7098   _spawn
 23033-23063  _spawn_from_flask
 16194-16435  _start_chat_listener
 11343-11360  _start_loop_watchdog
 10682-10710  _stats_loop
 10661-10664  _stats_output_path
 10667-10679  _stats_write
  7747-7763   _storage_cleanup_loop
 21877-21884  _story_for
  3106-3112   _stream_url_expiry
  3114-3119   _stream_url_ttl
 14525-14532  _streamer_persona_get
 19143-19265  _system_backup
 19274-19304  _system_backup_loop
  9866-9905   _test_proxy
 10412-10428  _testpush_resolve_live
  7203-7224   _tg_sprache_setzen
  7926-7936   _tg_topics_load_into_mem
  7923-7924   _tg_topics_path
  7938-7945   _tg_topics_save
  9274-9282   _token_ok
  7948-7952   _topic_forget
 11656-11667  _tracking_max_duration
  3896-3910   _tracking_remove_cleanup
  3927-3939   _tracking_resume_cleanup
  1522-1545   _try_attach_file_handler
 17909-17917  _tts_cleanup
 10388-10392  _tunnel_effective
 17405-17458  _twitch_channel_status
 20566-20711  _twitch_chat_loop
 20380-20483  _twitch_eventsub_loop
  1303-1316   _upload_queue_add
  1327-1329   _upload_queue_count
  1286-1295   _upload_queue_load
  1276-1278   _upload_queue_path
  1318-1325   _upload_queue_remove
  1297-1301   _upload_queue_save
  1331-1372   _upload_window_loop
  6951-6958   _uptime_s
 11966-11975  _url_host
   823-827    _usage_record_claude
  7141-7185   _verbindung_verloren
  6041-6072   _viewer_sample_loop
  9363-9366   _wants_html
  6961-6975   _warn_empty_env
 21611-21732  _watchdog_loop
 20119-20127  _wchat_thank_ok
 16028-16058  _whisper_get_model
  7048-7055   _whisper_native_section
 15230-15236  _whisper_pool
 16127-16156  _whisper_segments
 16060-16124  _whisper_transcribe
 12367-12529  _write_restream_overlay
 12329-12364  _write_restream_overlay_async
 20735-20815  _youtube_api_chat_loop
 17461-17564  _youtube_api_status
 17567-17634  _youtube_channel_status
 20818-20979  _youtube_chat_loop
 19979-19992  _youtube_restream_autoconfig
 19995-20019  _youtube_restream_autoconfig_inner
 20086-20114  _youtube_send
 17702-17743  _youtube_set_channel
 20022-20056  _yt_access_token
 20059-20074  _yt_live_chat_id
 20082-20083  _yt_sendrate_cfg
 20714-20729  _yt_timeout
  2857-2858   _ytdlp_detect_available
  2860-2871   _ytdlp_note_result
 11230-11232  _zombie_child_count
  6827-6851   about
  3807-3811   add_ai_log_entry
  3724-3727   add_archive_entry
  4321-4323   add_archive_rule
  4098-4132   add_recording
  3871-3888   add_tracking
  5428-5461   ai
  3459-3510   ai_chat
  3544-3554   ai_history_append
  3556-3561   ai_history_clear
  3533-3542   ai_history_load
  3518-3531   ai_rate_limit_check
  5490-5498   aireset
 15565-15584  azrael_chat
 20984-21106  brain_cmd
  3122-3127   build_recording_cmd
  3891-3894   bulk_add_trackings
  6295-6354   bulkadd
  7766-7906   check_all_trackings
  3943-3955   claim_live_transition
 14602-15162  class KickModerator
 12981-14365  class RestreamManager
 10271-10313  classify_proxy_anonymity
  5536-5734   cleanup
  4575-4581   cleanup_old_recordings
  4089-4096   clear_recording
 19736-19801  clip_moment
  4273-4276   compute_storage_forecast
  6417-6490   cookies_cmd
  3862-3868   count_trackings_for_chat
  3794-3805   decide_preferred_recorder
  3734-3737   delete_archive_entry
  4325-4327   delete_archive_rule
  4965-5112   diag
 21218-21279  einnahmen_cmd
  4267-4270   find_recordings_by_fingerprint
  3755-3771   finish_recording_attempt
  3915-3917   get_all_active_trackings
  3822-3824   get_all_checks
  4134-4137   get_all_recordings
  4216-4218   get_all_tags_with_counts
  4244-4247   get_annotations_for_recording
  3729-3732   get_archive_entry
  4237-4240   get_bookmarked_recordings
  2005-2151   get_cookie_health
  4204-4210   get_event_log
  3778-3792   get_last_recording_attempt
  2938-3043   get_live_status
  4514-4517   get_manual_recordings
  4252-4255   get_or_compute_inspect_sync
  4616-4619   get_outcome_breakdown
  4223-4226   get_priority_poll_interval
  3773-3776   get_recent_recording_attempts
  4139-4142   get_recording_by_id
  4230-4233   get_recording_note
  3260-3283   get_redis
  3851-3854   get_stats
  4569-4573   get_storage_stats
  4345-4347   get_tiktok_status_distribution
  3957-3966   get_tracking_state
  3912-3913   get_trackings_for_group
  4530-4533   get_trash_recordings
  8441-9109   handle_recording_finished
  3654-3679   init_db
  4317-4319   list_archive_rules
  4769-4807   live
  7281-7289   live_check_worker
  3338-3372   llm_chat
  3395-3423   llm_chat_sync
  3380-3392   llm_list_models
  4163-4196   log_event
  1590-1623   log_recording_failure
  6640-6689   logs_cmd
 21925-22428  main
  5464-5487   on_ai_media
  6766-6792   on_ai_reply
  6795-6824   on_azrael_mention
  6856-6886   on_callback
 15590-15694  oracle_handle
  6529-6532   pause_tracking
  4629-4634   profile_keyboard
  6591-6637   quota
  7670-7744   reaper_loop
  4341-4343   record_tiktok_status
  5503-5533   recstatus
  3285-3293   redis_get_json
  3296-3302   redis_set_json
 21282-21292  report_cmd
 10316-10318  report_proxy_result
  2400-2427   resolve_tiktok_live_stream
  4525-4528   restore_recording
  6535-6538   resume_tracking
  4330-4335   run_archive_rules
 21295-21518  run_bot
 11145-11197  run_flask
  4305-4308   sample_bandwidth_for_active
  3814-3820   save_tiktok_check
  4081-4087   set_recording_file
  3920-3924   set_tracking_paused
  4520-4523   soft_delete_recording
  8059-8439   split_and_send_video
  4682-4724   start
  3739-3753   start_recording_attempt
  5737-5775   stats
  4495-4512   stop_manual_recording
  6541-6588   stoprec
  5965-5973   summary_cmd
  6692-6763   sysres
  5114-5258   teststream
  4726-4767   tiktok
  6357-6414   topusers
  4844-4901   track
  4809-4841   track_exact
  4915-4963   tracklist
  4379-4493   trigger_manual_recording
  4042-4079   try_acquire_recording_lock
  4536-4538   universal_search
  4903-4913   untrack
 21109-21215  update_cmd
  4262-4265   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, get_archive_entries_paged, get_archive_entry, run_archive_file_check
archivename.py         open_unique
archiverules.py        add_archive_rule, delete_archive_rule, list_archive_rules, run_archive_rules
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            config, configure
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
backupcfg.py           aktiv, fehlgrund, lokal, lokal_dir, recordings_retain_days, retention_days, s3, s3_bucket, s3_endpoint, s3_konfiguriert, s3_region, s3_zugang, sys_backup, sys_hour, sys_keep, sys_max_file_mb
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
bandbreite.py          messen
binresolve.py          resolve
botctx.py              class BotKontext
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           configure, highlight_post, highlight_share_enabled, live_ping, live_ping_enabled, note_chatter, returning_enabled, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookieholen.py         aktualisiere, aus_browser, configure, hole_gastcookies, schreibe, zusammenfuehren
cookies.py             configure, lade_jar, load_dict
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dashauth.py            geschuetzt, host, lage, nur_lokal, offen_im_netz
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              configure_db, db_async, db_conn, get_pool, set_pool
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordlimits.py       aktuell_label, aktuell_mb, configure, describe, effective_upload_mb, gate_mb, guild_filesize_bytes, guild_limit_mb
discordstate.py        invite, state_get
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventlog.py            leeren, schreibe, stand
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
fehlertext.py          nach_aussen, saeubern
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      drawtext_chain, studio_chain
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, last_errors, list_models_sync
geocache.py            get, groesse, leeren, put
geoip.py               ist_privat, lookup
highlights.py          check, new_state, observe, score, zustand
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             app_token, broadcaster_id, channel_info, configure, oauth_exchange, search_category, send_message, slug, timeout_user, update_channel, user_token
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             redact_stream_urls, url_ohne_zugang
loyalty.py             award_chat, award_return, configure, enabled, leaderboard, rank_for, status
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modki.py               frage, lies_klassifikation, lies_schimpfwoerter
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
outcomes.py            get_outcome_breakdown
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
qrsvg.py               qr_svg
reccmd.py              build_recording_cmd, configure
recdb.py               configure, find_recordings_by_fingerprint, get_all_checks, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, fenstergroesse, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, url_host
restreamcfg.py         active_platforms, aktiv, bereite_ziele, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamcmd.py         build, configure
restreamgesundheit.py  blind_markieren, frische_tee_fehler, marke_setzen
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              create_schema
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sicherpfad.py          pruefe_unter, sicher_join, sicherer_name, unter
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
storage.py             cleanup, forecast, stats
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
suche.py               universal_search
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
systemprobe.py         active_recorder, ai_alive, ai_calls_total, cache_leeren, cached_probe, configure, cpu_load_snapshot, disk_pct, recorder_pref, recordings_dir, redis_alive, redis_url, redis_version
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
twitchoauth.py         access_token, authorize_url, configure, exchange_code, forget, login_name, search_category, status, timeout_user, update_channel
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             build_stamp, changelog, current, latest, summary_line
videoteil.py           configure, dauer, ist_kaputter_container, kopier_teilen, neu_kodieren, platz_reicht, reparieren, wegwerfen, zeitstempel_richten, zu_gross
whispercfg.py          geladen, name, verfuegbar, waehle
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DiskAgent, class HealthAgent, class LearningAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```
