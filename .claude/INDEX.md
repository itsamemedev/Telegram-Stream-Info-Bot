# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
  9864  GET              /                                                dashboard
 11911  GET              /api/abo/status                                  api_abo_status
 11865  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 10652  GET              /api/automation/status                           api_automation_status
 10674  POST             /api/automation/toggle                           api_automation_toggle
 19204  GET              /api/channel/categories                          api_channel_categories
 19210  POST             /api/channel/set                                 api_channel_set
 19057  GET              /api/channels/status                             api_channels_status
 18731  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 18714  GET              /api/clips                                       api_clips
 18760  POST/DELETE      /api/clips/clear                                 api_clips_clear
 18639  GET              /api/debug/threads                               api_debug_threads
 11876  GET              /api/events                                      api_events
 11360  GET              /api/events/stream                               api_events_stream
 11187  GET              /api/health                                      api_health
 18673  POST             /api/highlights/config                           api_highlights_config
  9798  POST             /api/login                                       dashboard_login_submit
 12201  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 11275  GET              /api/notify/status                               api_notify_status
 11286  POST             /api/notify/test                                 api_notify_test
 11965  GET              /api/proxy/heatmap                               api_proxy_heatmap
 11942  GET              /api/proxy/trend                                 api_proxy_trend
 18780  GET              /api/tts/<fn>                                    api_tts_file
 19555  GET              /api/upload_window                               api_upload_window
 11477  GET              /archive/<int:eid>/download                      archive_download
 11505  GET              /download/<int:recording_id>                     download
 11434  GET              /health                                          health
 18585  GET              /healthz                                         healthz
  9789  GET              /login                                           dashboard_login_page
  9819  GET              /logout                                          dashboard_logout
  9826  GET              /manifest.webmanifest                            pwa_manifest
 19528  GET              /overlay                                         overlay_page
  9850  GET              /pwa-icon-<variant>.png                          pwa_icon
  9836  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (338)

```
   183  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   410  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
   195  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   165  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
   993  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   738  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   864  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   844  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   882  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   806  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   356  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   367  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   377  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   400  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   407  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   418  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   546  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   644  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1231  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1263  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   341  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   946  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   926  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1099  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1147  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1198  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1057  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   901  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   499  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   763  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   645  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   628  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   620  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   456  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   472  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   807  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   374  GET              /api/archive/scan                                api_archive_scan   [nc/routes/archive.py]
   405  POST             /api/archive/scan/adopt                          api_archive_scan_adopt   [nc/routes/archive.py]
   772  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   792  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   679  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
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
   387  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
   364  GET              /api/bookmarks                                   api_bookmarks_list   [nc/routes/auskunft.py]
   198  GET              /api/brain                                       api_brain   [nc/routes/brain.py]
   131  GET              /api/brain/alarms                                api_brain_alarms   [nc/routes/brain.py]
   116  GET              /api/brain/creator                               api_brain_creator   [nc/routes/brain.py]
    93  GET              /api/brain/graph                                 api_brain_graph   [nc/routes/brain.py]
   158  GET              /api/brain/growth                                api_brain_growth   [nc/routes/brain.py]
    80  GET              /api/brain/health                                api_brain_health   [nc/routes/brain.py]
    81  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    53  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
   162  GET              /api/checks                                      api_checks   [nc/routes/auskunft.py]
    40  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    52  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    52  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    87  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   122  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   431  GET              /api/community/stats                             api_community_stats   [nc/routes/auskunft.py]
   433  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   418  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   238  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
   195  POST             /api/cookies/fetch                               api_cookies_fetch   [nc/routes/settings.py]
    73  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    80  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   485  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   259  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   286  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   379  POST             /api/db/restore/apply                            api_db_restore_apply   [nc/routes/settings.py]
   323  GET              /api/db/restore/list                             api_db_restore_list   [nc/routes/settings.py]
   341  POST             /api/db/restore/prepare                          api_db_restore_prepare   [nc/routes/settings.py]
   246  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
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
   382  GET              /api/forecast/storage                            api_forecast_storage   [nc/routes/auskunft.py]
   285  GET              /api/freeai/status                               api_freeai_status   [nc/routes/auskunft.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   402  GET              /api/heatmap/lives/<username>                    api_heatmap_lives   [nc/routes/auskunft.py]
   397  GET              /api/heatmap/recordings                          api_heatmap_recordings   [nc/routes/auskunft.py]
   473  GET              /api/highlights                                  api_highlights   [nc/routes/auskunft.py]
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
    66  GET              /api/lagebild                                    api_lagebild   [nc/routes/lagebild.py]
   416  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard   [nc/routes/auskunft.py]
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
   257  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   324  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   352  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   203  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   270  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   505  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    80  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   168  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   151  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   391  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   226  GET              /api/outcomes                                    api_outcomes   [nc/routes/auskunft.py]
   210  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   193  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
    94  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   177  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   460  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   435  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   296  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   143  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   944  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
  1053  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
  1081  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
  1101  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   931  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   993  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   980  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   961  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   335  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   606  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   601  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   649  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   532  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   859  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   623  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   586  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   559  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   833  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   703  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   792  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   698  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   631  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   411  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   876  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   499  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   754  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   909  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   894  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   455  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   693  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   679  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   662  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   719  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
  1244  GET              /api/recordings/session/<sid>                    api_recording_session   [nc/routes/recordings.py]
  1319  POST             /api/recordings/session/<sid>/join               api_recording_session_join   [nc/routes/recordings.py]
  1208  GET              /api/recordings/sessions                         api_recording_sessions   [nc/routes/recordings.py]
   812  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   708  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
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
   474  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   464  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   499  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    65  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    86  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    52  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
   102  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   354  GET              /api/search                                      api_search   [nc/routes/auskunft.py]
    92  GET              /api/selftest                                    api_selftest   [nc/routes/selbsttest.py]
   444  GET              /api/shield/stats                                api_shield_stats   [nc/routes/auskunft.py]
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
   207  GET              /api/summary/preview                             api_summary_preview   [nc/routes/auskunft.py]
    73  GET              /api/system                                      api_system   [nc/routes/systemlage.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   177  GET              /api/system/check_timing                         api_check_timing   [nc/routes/systemlage.py]
   117  GET              /api/system/config_drift                         api_config_drift   [nc/routes/systemlage.py]
   140  GET              /api/system/config_snapshot                      api_system_config_snapshot   [nc/routes/systemlage.py]
   237  GET              /api/system/preflight                            api_system_preflight   [nc/routes/systemlage.py]
   104  GET              /api/system/preflight_history                    api_system_preflight_history   [nc/routes/systemlage.py]
   369  GET              /api/system/resilience                           api_system_resilience   [nc/routes/systemlage.py]
   377  GET              /api/tags                                        api_tags_list   [nc/routes/auskunft.py]
   177  GET              /api/top                                         api_top   [nc/routes/auskunft.py]
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
   253  GET              /api/trend-7d                                    api_trend_7d   [nc/routes/auskunft.py]
   121  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
   100  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   132  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
   113  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   125  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    77  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
   101  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    55  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   453  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   419  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   478  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   458  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   441  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   434  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
   239  GET              /api/userstats                                   api_userstats   [nc/routes/auskunft.py]
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
    73  GET              /fonts/<name>                                    schrift   [nc/routes/schriften.py]
    66  GET              /fonts/schriften.css                             schriften_css   [nc/routes/schriften.py]
   382  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
```

## Discord-Slash-Commands in discordbot.py (65)

```
  2080  /about                  Ueber diesen Bot
   809  /ai                     
  2080  /aireset                KI-Kontext zuruecksetzen
  1213  /ask                    
   910  /assign_role            
   960  /ban                    
  2035  /botstats               
  2080  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2080  /bulkadd                Mehrere User auf einmal tracken · a b c
  2080  /cleanup                Alte Aufnahmen aufraeumen
  1468  /clearwarns             
  1999  /clip                   
  1984  /clipoftheweek          
  1339  /clips                  
  2080  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
   865  /create_category        
   836  /create_channel         
   900  /create_group           
   875  /create_role            
   851  /create_voice           
  1096  /daily                  
  2080  /diag                   Vollstaendige Diagnose
  2080  /einnahmen              Einnahmen und Spenden
  1242  /event                  
  1284  /events                 
  1378  /follow                 
  1367  /help                   
   950  /kick                   
  1071  /leaderboard            
  2080  /live                   Live-Status sofort pruefen · @user
  1326  /livenow                
  2080  /logs                   Letzte Fehler aus dem Log
  2080  /pause                  Tracking pausieren · @user
  1354  /post_test              
  1174  /profile                
   982  /purge                  
  2080  /quota                  Speicher-Quota
  1058  /rank                   
  1314  /recstatus              
   920  /remove_role            
  2080  /report                 Azrael-Sentinel-Wochenreport
   822  /restream_status        
  2080  /resume                 Tracking fortsetzen · @user
   930  /set_channel_perms      
  1025  /setup_community        
  1042  /setup_targets          
  1410  /stats                  
   781  /status                 
  2080  /stoprec                Laufende Aufnahme sauber beenden · @user
  1506  /streaminfo             
  2080  /summary                Tageszusammenfassung
  2080  /sysres                 System-Ressourcen
  2080  /teststream             Recorder-Selbsttest · @user
  2080  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
   970  /timeout                
  1478  /topstreamers           
  2080  /topusers               Top-Streamer nach Aufnahmen
   711  /track                  
  2080  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
   794  /tracklist              
  1392  /unfollow               
  2080  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
   743  /untrack                
  1431  /warn                   
  1454  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2238  on_member_join
  2200  on_message
  2101  on_raw_reaction_add
  2273  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    58-73     konfiguriere
    76-456    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (46 Funktionen)

```
  1583-1634   _award_xp
  1803-1832   _clip_week_leader
  1856-1870   _clipoftheweek_loop
  2389-2451   _community_events_loop
  1540-1562   _dc_client
  1565-1574   _dc_offen
  2491-2526   _disc_automod_check
   401-406    _disc_sprache_setzen
  1637-1685   _discord_ai_automod
   534-573    _discord_automod
  1688-1708   _discord_azrael_reply
  1873-2348   _discord_run_once
   236-294    _discord_start
   297-351    _ensure_discord_invite
  2354-2386   _ensure_error_channel
   422-435    _ensure_rank_roles
   674-688    _ensure_team_roles
  2454-2484   _error_channel_loop
   583-587    _guard
   503-531    _handle_voice_ai
   409-419    _is_admin
  1751-1762   _liveboard_loop
   590-608    _on_level_up
   499-500    _par_chat_id
  1835-1853   _post_clip_of_week
  1765-1783   _post_weekly_digest
   438-464    _provision_base_channels
   467-483    _provision_user_channels
  1306-1399   _reg_betrieb
   996-1085   _reg_community_setup
  1088-1163   _reg_daily_profil
  1206-1303   _reg_frage_events
   768-824    _reg_info
   942-993    _reg_moderation
  1166-1203   _reg_profil
   891-939    _reg_rollen
   827-888    _reg_server
  1402-1489   _reg_streamer
  1492-1537   _reg_system
   702-765    _reg_tracking
   643-671    _run_tg_handler
   486-496    _tracked_usernames
   153-215    _uebernehmen
  1717-1748   _update_liveboard
  1786-1800   _weekly_digest_loop
   218-221    starte
```

## Top-Level-Symbole in bot.py (517 Funktionen, 2 Klassen)

```
 24094-24116  _abbruch_datenbank_unlesbar
  2623-2624   _abo_key
  2644-2662   _abo_probe_dump
 24167-24185  _abschluss
 15510-15517  _ad_allowlist
 16490-16496  _agent_for
 16499-16515  _ai_telemetry
 17010-17028  _alert
 20415-20465  _alert_monitor_loop
 20817-20879  _announce_loop
  3476-3486   _anthropic_key
  3493-3495   _anthropic_model
  9481-9484   _arg_int
  2615-2620   _as_dict
 23844-23853  _async_exc_handler
 17191-17213  _audio_tap_cmd
 17771-17830  _audio_tap_melden
 17227-17251  _audio_tap_sammler
 24119-24154  _aufraeumen
  9652-9721   _auth_cookie
  9619-9648   _auth_guard
  1874-1879   _auto_on
 18447-18465  _auto_restream_loop
 13381-13423  _avatar_frames_laden
 21897-21912  _azrael_broadcast_reply
 21797-21819  _azrael_chat_reply
 21769-21794  _azrael_chat_should_reply
 21825-21827  _azrael_gate_cfg
 16520-16534  _azrael_live_state
 19441-19455  _azrael_overlay_state
 16892-16946  _azrael_proactive_loop
 16338-16394  _azrael_reaction_to_chats
 21830-21837  _azrael_reply_all_chats
 21756-21766  _azrael_self_names
 21865-21894  _azrael_send_to
 13342-13378  _azrael_spricht
 16540-16561  _azrael_system
 20549-20552  _backup_active
 20630-20643  _backup_loop
 23917-23926  _brain_crowdsec_snap
 20336-20345  _brain_growth_loop
 10043-10070  _brain_growth_snapshot
  2557-2577   _brain_hint_delay
 23989-24024  _brain_moderation_snap
  6372-6400   _brain_notify
 24027-24049  _brain_recording_snap
 23929-23986  _brain_restream_health
 24052-24065  _brain_tiktok_status_snap
 11339-11356  _browser_push
  6412-6499   _build_daily_summary
 13702-13706  _build_restream_cmd
  5194-5221   _can_stop_tracking
  1987-2009   _capture_set_cookies
 12019-12022  _cfg_get
 12025-12027  _cfg_set
 19165-19200  _channel_set_all
 12570-12573  _chat_connected
 12576-12592  _chat_disconnected
  8538-8549   _chat_is_forum
 17578-17603  _chat_listener_abbauen
 12612-12614  _chat_sanitize
 12555-12567  _chat_stat
 12595-12598  _chat_stats_snapshot
  3788-3800   _check_ai_models_sync
 10325-10368  _classify_pool_anonymity
 10371-10388  _classify_pool_anonymity_bg
   870-892    _claude_chat_sync_metered
  9513-9520   _client_ip
 20963-20990  _clip_prune
 20993-21003  _clip_recfile_for
 21413-21419  _clip_should_velocity
 21044-21126  _clip_to_discord
  3674-3683   _close_ai_session
 21943-21958  _cohost_broadcast
 21928-21929  _cohost_cfg
 21984-21996  _cohost_fire_highlight
 21932-21940  _cohost_gate
 21961-21981  _cohost_highlight
  9973-9975   _conv_messages
  6771-6832   _cookie_alarm_loop
  2077-2078   _cookie_autofetch_info
  2061-2065   _cookie_autorefresh_info
 23554-23576  _cookie_bezug_loop
 23579-23604  _cookie_bezug_runde
  1964-1968   _cookie_header
  2090-2104   _cookies_selbst_holen
  4024-4036   _create_index_safe
 19887-19993  _crowdsec_status
 19833-19884  _crowdsec_via_lapi
 19737-19755  _cscli_bin
 19764-19777  _cscli_path
  6661-6686   _daily_summary_loop
 19795-19812  _darf_journal_lesen
  3040-3065   _darf_ytdlp_nachschlagen
 11520-11541  _dashboard_adresse
 20389-20412  _db_maintenance_loop
  6630-6658   _db_vacuum_loop
 15533-15557  _detect_foreign_ad
  1555-1566   _diag_path_owner
 16798-16842  _director_finalize
 17760-17767  _director_for
 16747-16795  _director_mark
 21278-21281  _disc_state_get
 21284-21291  _disc_state_set
 20317-20326  _discord_bot_starten
 20280-20291  _discord_einladung_merken
 20329-20333  _discord_invite
 20294-20314  _discord_kontext
 21239-21275  _discord_live_thread
 16949-16961  _discord_notify
 20252-20277  _discord_ops_alert
 21137-21235  _discord_post_user
 20882-20888  _discord_stop
  6689-6766   _disk_alarm_loop
 23479-23528  _disk_autoclean
 23699-23712  _disk_guard_loop
 13320-13327  _drossel_hoeher
 13316-13317  _drossel_stufe
 13330-13338  _drossel_zuruecksetzen
 11697-11699  _dump_all_threads
 10251-10314  _enrich_proxies_with_geo
  2133-2194   _ensure_cookie_file_netscape
  8597-8600   _ensure_notify_topic
 10495-10532  _ensure_proxy_ready
  8551-8578   _ensure_topic
   719-721    _env_int
   724-726    _env_int_range
 16994-17007  _event_webhook
 12370-12383  _evolution_loop
  5814-5848   _extract_file_payload
  2266-2268   _extract_urls_from_streamurl_node
 19780-19787  _f2b_sudo_hint
 24188-24251  _fatal_vom_botteil
  4658-4668   _fehler_text
 10152-10170  _fetch_proxy_list
 17547-17575  _fetch_tiktok_room_id
   802-805    _ff_cmd
 13149-13154  _find_chromium
  3396-3398   _find_external_recorder
  2271-2273   _find_stream_urls
 12070-12095  _fire_webhooks
  7598-7607   _fork_safe
   903-916    _freeai_chat_sync_metered
 19826-19830  _geo_lookup_ips
  3662-3671   _get_ai_session
  7431-7471   _get_live_info
  2889-2896   _get_resolve_semaphore
  7880-8252   _handle_single_tracking
 23301-23303  _hb
 23306-23323  _hb_while
 12626-12628  _highlight_cfg
 12631-12660  _highlight_observe
 13157-13175  _htmlov_screenshot_cmd
 17253-17263  _httpx_proxy
 12103-12115  _in_quiet_hours
 24080-24091  _init_db_oder_abbruch
 24828-24859  _install_fast_eventloop
  9376-9430   _install_fast_json
 11702-11718  _install_faulthandler
 18493-18502  _intel_ensure_schema
 18540-18575  _intel_index_loop
 18514-18524  _intel_index_one
 18505-18511  _intel_semantic
  5183-5192   _is_authorized
  7781-7787   _is_dead
  2256-2258   _is_hevc
 19815-19817  _is_private_ip
  1773-1780   _is_process_running
  6402-6409   _is_quiet_hours
  1348-1357   _is_upload_window
  4523-4538   _iso
  9465-9478   _json_error_handler
  6624-6625   _kick_broadcaster_id
  6536-6578   _kick_follower_count
  6520-6523   _kick_slug
 11152-11159  _kick_user_token
 24068-24077  _kickmod_boot
  4113-4116   _kind_from_filename
 12132-12134  _latest_popularity
  1710-1719   _laufstand
 23662-23696  _laufstand_loop
 18156-18205  _live_react_loop
 17833-18145  _live_react_worker
 16397-16408  _live_transcript_push
 18147-18154  _live_users
 16845-16889  _living_title_loop
 20555-20627  _local_backup_scan
  9447-9461   _log_5xx
   792-799    _log_sicher
 13714-13726  _looks_like_codec_err
 13709-13711  _looks_like_source_expired
  7648-7678   _loop_fehler
 11722-11731  _loop_heartbeat
 23271-23298  _loop_lag_monitor
 11734-11802  _loop_watchdog_thread
 16277-16291  _loyalty_add
 16268-16274  _loyalty_get
 16294-16302  _loyalty_top
 12242-12244  _manual_donations_total
  4865-4884   _manual_status
  7789-7790   _mark_dead
 10771-10787  _marketing_loop
 21844-21862  _maybe_handle_command
 23798-23822  _maybe_hype_clip
 20932-20960  _meme_klassifizieren
  3991-4014   _migrate_columns
 22123-22134  _mod_is_exempt
 22137-22142  _mod_warn_first
 22145-22148  _mod_warn_text
 12410-12418  _modlog
  1048-1050   _multistream_targets
  3068-3104   _nachschlag_ytdlp
  7610-7611   _nc_create_subprocess_exec
  7614-7615   _nc_create_subprocess_shell
 11089-11106  _news_loop
 12437-12439  _normalize_ingest
  2488-2505   _note_check_duration
  8591-8594   _notify_topic_name
  3107-3127   _ohne_url_melden
 16423-16431  _oracle_memories
 16696-16730  _oracle_memorize
 16434-16447  _oracle_persona
 16416-16420  _oracle_recent_text
 12783-12784  _ov_atomic_write
 12774-12776  _ov_bar
 15436-15448  _ov_clip_text
 12779-12780  _ov_oneline
 19492-19521  _overlay_push
 13103-13146  _overlay_render_size
 12506-12510  _overlay_session_reset
 19457-19459  _overlay_src_ok
 15520-15530  _own_invites
 13098-13100  _parse_size
 20001-20081  _parse_ssh_attacks
  7033-7066   _pause_resume_cmd
  2015-2059   _persist_refreshed_cookies
  1918-1950   _pick_checked_pull_proxy
  9549-9562   _pin_auth_value
  9608-9609   _pin_clear_fail
  9588-9591   _pin_locked
  9594-9605   _pin_note_fail
  9565-9585   _pin_ok
 19301-19326  _piper_pick_model
 19386-19435  _piper_say
 12032-12067  _post_json_threaded
 13077-13095  _probe_video_size
  1801-1818   _proc_is_recorder
 10464-10492  _proxy_pool_refresh_loop
  1884-1915   _proxy_report_recording
 11687-11689  _prune_stall_dumps
 10841-11011  _public_stats
  2081-2087   _pull_proxy_still
 16965-16991  _push_notify
  9768-9770   _pwa_dir
 10221-10236  _quick_validate_proxy
 12098-12100  _quiet_hours_config
  9733-9766   _rate_guard
 16238-16244  _react_warn
  7518-7557   _reap_proc
  8825-8892   _rec_auto_abschalten
  8772-8822   _rec_frueh_getrennt
  8655-8717   _rec_kategorie_melden
  8720-8769   _rec_totstreak_fortschreiben
  2528-2550   _record_check_outcome
   787-789    _redact_stream_urls
 10391-10461  _refresh_proxy_pool
  2305-2396   _resolve_via_html
  2669-2866   _resolve_via_webcast_api_v2
  2929-3016   _resolve_via_ytdlp
 21453-21582  _resolve_youtube_ingest
  2282-2302   _resolver_stumm
 12489-12500  _restream_active_sources
 13426-13550  _restream_avatar_feeder_start
 13553-13562  _restream_avatar_feeder_stop
 17606-17724  _restream_chat_guardian
 12663-12735  _restream_chat_push
 12760-12769  _restream_chat_push_async
 13178-13287  _restream_html_overlay_start
 13290-13303  _restream_html_overlay_stop
 12448-12471  _restream_overlay_files
 18209-18241  _restream_platform_state
 18409-18444  _restream_resume_after_restart
 13610-13668  _restream_tts_enqueue_wav
 13039-13071  _restream_tts_feeder
 13036-13037  _restream_tts_fifo_path
 13565-13592  _restream_tts_start
 13594-13608  _restream_tts_stop
 18247-18406  _restream_verify_loop
 20520-20532  _retention_loop
 20514-20517  _retention_scan
  2626-2628   _room_is_abo
  5852-5969   _run_ai_call
 11825-11838  _run_async_from_flask
 19820-19823  _run_priv
 24816-24824  _run_selfcheck_and_exit
 20535-20546  _s3_client
  7816-7867   _safe_send
  4791-4807   _sample_net_throughput
  2580-2601   _schedule_next_check
 20468-20511  _scheduler_loop
  4017-4021   _schema_pk
 11842-11847  _scraper_session
 22151-22190  _screen_full
 11203-11240  _sec_headers
  2261-2263   _select_stream_from_data_section
 24541-24813  _selfcheck
  8603-8637   _send_live_notice
  1371-1375   _should_defer_upload
 21006-21041  _shrink_for_discord
  9773-9785   _sicheres_ziel
 20348-20386  _sicherheits_erinnerung_loop
 23719-23736  _sign_health_check
 23739-23758  _sign_health_loop
  4541-4566   _sitzung_bestimmen
  7627-7638   _spawn
 25241-25271  _spawn_from_flask
 17265-17544  _start_chat_listener
 11805-11822  _start_loop_watchdog
 11038-11084  _stats_loop
 11017-11020  _stats_output_path
 11023-11035  _stats_write
 19338-19352  _stimme_saubern
 19359-19383  _stimme_schon_gesagt
  8331-8347   _storage_cleanup_loop
 23778-23785  _story_for
  3421-3427   _stream_url_expiry
  3429-3434   _stream_url_ttl
 15483-15490  _streamer_persona_get
 20652-20774  _system_backup
 20783-20813  _system_backup_loop
 11647-11665  _task_auf_bot_schleife
 22964-22980  _telegram_befehlsmenue
  7681-7727   _telegram_polling_fehler
 10173-10212  _test_proxy
 10719-10735  _testpush_resolve_live
  7792-7813   _tg_sprache_setzen
  8510-8520   _tg_topics_load_into_mem
  8507-8508   _tg_topics_path
  8522-8529   _tg_topics_save
  9523-9531   _token_ok
  8532-8536   _topic_forget
 12118-12129  _tracking_max_duration
  4321-4335   _tracking_remove_cleanup
  4352-4364   _tracking_resume_cleanup
  1613-1636   _try_attach_file_handler
 19328-19336  _tts_cleanup
 10695-10699  _tunnel_effective
 23531-23551  _tunnel_lage
 23607-23659  _tunnel_wacht_loop
 18824-18877  _twitch_channel_status
 22193-22338  _twitch_chat_loop
 21297-21310  _twitch_clip_versuchen
 22007-22110  _twitch_eventsub_loop
  1394-1407   _upload_queue_add
  1418-1420   _upload_queue_count
  1377-1386   _upload_queue_load
  1367-1369   _upload_queue_path
  1409-1416   _upload_queue_remove
  1388-1392   _upload_queue_save
  1422-1463   _upload_window_loop
  7491-7498   _uptime_s
 12425-12434  _url_host
  3130-3224   _url_nachschlag
   863-867    _usage_record_claude
 23892-23914  _v37_pause_source
 23856-23866  _v37_restream_restart
 23869-23889  _v37_unpause_source
  7730-7774   _verbindung_verloren
  6581-6612   _viewer_sample_loop
  9612-9615   _wants_html
  7501-7515   _warn_empty_env
 23344-23465  _watchdog_loop
 21728-21736  _wchat_thank_ok
 17033-17063  _whisper_get_model
  7588-7595   _whisper_native_section
 16225-16231  _whisper_pool
 17157-17189  _whisper_segments
 17065-17081  _whisper_stumm
 17084-17154  _whisper_transcribe
 12831-12993  _write_restream_overlay
 12793-12828  _write_restream_overlay_async
 22362-22458  _youtube_api_chat_loop
 18880-18983  _youtube_api_status
 18986-19053  _youtube_channel_status
 22461-22622  _youtube_chat_loop
 21313-21338  _youtube_clip_versuchen
 21588-21601  _youtube_restream_autoconfig
 21604-21628  _youtube_restream_autoconfig_inner
 21695-21723  _youtube_send
 19121-19162  _youtube_set_channel
 21631-21665  _yt_access_token
 21668-21683  _yt_live_chat_id
 21691-21692  _yt_sendrate_cfg
 22341-22356  _yt_timeout
  2913-2914   _ytdlp_detect_available
  2916-2927   _ytdlp_note_result
 11692-11694  _zombie_child_count
  7367-7391   about
  4232-4236   add_ai_log_entry
  4149-4152   add_archive_entry
  4829-4831   add_archive_rule
  4569-4640   add_recording
  4296-4313   add_tracking
  5972-6005   ai
  3814-3895   ai_chat
  3929-3939   ai_history_append
  3941-3946   ai_history_clear
  3918-3927   ai_history_load
  3903-3916   ai_rate_limit_check
  6034-6042   aireset
 16564-16583  azrael_chat
 22627-22749  brain_cmd
  3437-3442   build_recording_cmd
  4316-4319   bulk_add_trackings
  6835-6894   bulkadd
  8350-8490   check_all_trackings
  4368-4380   claim_live_transition
 15560-16157  class KickModerator
 13729-15323  class RestreamManager
 10578-10620  classify_proxy_anonymity
  6080-6278   cleanup
  5119-5125   cleanup_old_recordings
  4514-4521   clear_recording
 21341-21410  clip_moment
  4781-4784   compute_storage_forecast
  6957-7030   cookies_cmd
  4287-4293   count_trackings_for_chat
  4219-4230   decide_preferred_recorder
  4159-4162   delete_archive_entry
  4833-4835   delete_archive_rule
  5509-5656   diag
 22861-22922  einnahmen_cmd
  4775-4778   find_recordings_by_fingerprint
  4180-4196   finish_recording_attempt
  4340-4342   get_all_active_trackings
  4247-4249   get_all_checks
  4642-4645   get_all_recordings
  4724-4726   get_all_tags_with_counts
  4752-4755   get_annotations_for_recording
  4154-4157   get_archive_entry
  4745-4748   get_bookmarked_recordings
  2121-2126   get_cookie_health
  4712-4718   get_event_log
  4203-4217   get_last_recording_attempt
  3227-3358   get_live_status
  5058-5061   get_manual_recordings
  4760-4763   get_or_compute_inspect_sync
  5160-5163   get_outcome_breakdown
  4731-4734   get_priority_poll_interval
  4198-4201   get_recent_recording_attempts
  4647-4650   get_recording_by_id
  4738-4741   get_recording_note
  3608-3631   get_redis
  4276-4279   get_stats
  5113-5117   get_storage_stats
  4853-4855   get_tiktok_status_distribution
  4382-4391   get_tracking_state
  4337-4338   get_trackings_for_group
  5074-5077   get_trash_recordings
  8895-9355   handle_recording_finished
 22956-22961  hilfe_cmd
  4044-4104   init_db
  4825-4827   list_archive_rules
  5313-5351   live
  7870-7878   live_check_worker
  3686-3725   llm_chat
  3748-3778   llm_chat_sync
  3733-3745   llm_list_models
  4671-4704   log_event
  1735-1768   log_recording_failure
  7180-7229   logs_cmd
 24254-24531  main
  6008-6031   on_ai_media
  7306-7332   on_ai_reply
  7335-7364   on_azrael_mention
  7396-7426   on_callback
 16589-16693  oracle_handle
  7069-7072   pause_tracking
  5173-5178   profile_keyboard
  7131-7177   quota
  8254-8328   reaper_loop
  4849-4851   record_tiktok_status
  6047-6077   recstatus
  3633-3641   redis_get_json
  3644-3650   redis_set_json
 22983-22993  report_cmd
 10623-10625  report_proxy_result
  2399-2441   resolve_tiktok_live_stream
  5069-5072   restore_recording
  7075-7078   resume_tracking
  4838-4843   run_archive_rules
 22996-23251  run_bot
 11544-11638  run_flask
  4813-4816   sample_bandwidth_for_active
  4239-4245   save_tiktok_check
  4506-4512   set_recording_file
  4345-4349   set_tracking_paused
  5064-5067   soft_delete_recording
  8643-8653   split_and_send_video
  5226-5268   start
  4164-4178   start_recording_attempt
  6281-6319   stats
  5003-5056   stop_manual_recording
  7081-7128   stoprec
  6505-6513   summary_cmd
  7232-7303   sysres
  5658-5802   teststream
  5270-5311   tiktok
  6897-6954   topusers
  5388-5445   track
  5353-5385   track_exact
  5459-5507   tracklist
  4887-5001   trigger_manual_recording
  4467-4504   try_acquire_recording_lock
  5080-5082   universal_search
 22925-22953  unpause_cmd
  5447-5457   untrack
 22752-22858  update_cmd
  4770-4773   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, class BestandUnbekannt, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, finde_ohne_eintrag, get_archive_entries_paged, get_archive_entry, run_archive_file_check, uebernehmen
archivename.py         open_unique
archiverules.py        add_archive_rule, delete_archive_rule, list_archive_rules, run_archive_rules
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            config, configure
audiotap.py            diagnose, melden, warum_kein_tap
aufnahmefolge.py       aufnahme_geglueckt, daten_geflossen, melden_erlaubt, nach_403, nach_frueher_trennung, nach_totem_versuch, sitzung_zuende, sperre_rest
aufnahmekategorie.py   kategorisiere
aufnahmesitzung.py     abdeckung, concat_cmd, concat_liste, gehoert_dazu, luecken, sekunden, sitzung_id, zieldatei
auslieferung.py        schreibe, stand, text
avatarloop.py          blinzeln, ruhe_seit, schleife, zustand
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
backupcfg.py           aktiv, fehlgrund, lokal, lokal_dir, recordings_retain_days, retention_days, s3, s3_bucket, s3_endpoint, s3_konfiguriert, s3_region, s3_zugang, sys_backup, sys_hour, sys_keep, sys_max_file_mb
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
bandbreite.py          messen
befehle.py             beschreibung, discord_nativ, discord_ueber_tg, fuer, hilfe_text, pruefen, telegram_handler
binresolve.py          resolve
botctx.py              class BotKontext
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatfolge.py           entscheide
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           anzeigename, configure, darf_pingen, highlight_post, highlight_share_enabled, live_ping, live_ping_enabled, note_chatter, returning_enabled, rollen_id, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookiebezug.py         anstossen, configure, faellig, gast_hilft, holen, info, intervall_s, naechster_lauf
cookieholen.py         aktualisiere, aus_browser, configure, hole_gastcookies, schreibe, zusammenfuehren
cookies.py             configure, gesundheit, lade_jar, load_dict
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, erwartete_namen, fehlende_namen, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dashauth.py            erlaubt_offen, geschuetzt, host, lage, nur_lokal, offen_im_netz, zurueckgefallen
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbrestore.py           archive, dump_aus_archiv, einsetzen, einspielen, vorbereiten
dbwrap.py              class DatenbankUnlesbar, configure_db, datei_diagnose, db_async, db_conn, get_pool, set_pool
ddlsafe.py             ddl, ist_schon_da
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordlimits.py       aktuell_label, aktuell_mb, configure, describe, effective_upload_mb, gate_mb, guild_filesize_bytes, guild_limit_mb
discordrang.py         rang_fuer_level, slug, xp_fuer_level, xp_zu_level
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
ffmpeg_filters.py      avatar_kette, chat_umbruch_w, chat_zeilen, drawtext_chain, studio_chain, studio_masse
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, dienstmeldung, katalog_kennt, last_errors, list_models_sync, stream_haeppchen, stream_rest
geocache.py            get, groesse, leeren, put
geoip.py               ist_privat, lookup
highlights.py          check, new_state, observe, score, zustand
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             app_token, broadcaster_id, channel_info, configure, oauth_exchange, search_category, send_message, slug, timeout_user, update_channel, user_token
kiwahl.py              backend, lokal_stand, lokal_zuerst, normal, provider
lagebild.py            bauen, restream_lage
lastvorsorge.py        freie_kerne, jung, startstufe
laufstand.py           befehl, veraltet, vergleich
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
livecache.py           aufraeumen, frisch, holen, setzen
livefolge.py           braucht_url_nachschlag, hat_stream_url, live_gesehen, offline_bestaetigt, poll_abstand, ruhezeit
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             fuer_log, redact_cookie_zeilen, redact_pull_urls, redact_stream_urls, url_ohne_zugang
logschleuse.py         class Schleuse, entkoppeln, stoppen, verloren, wartend, zuruecksetzen
loyalty.py             award_chat, award_return, configure, enabled, leaderboard, rank_for, status
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
meldetakt.py           melden, zuruecksetzen, zusatz
memeklip.py            class Fenster, frage, lies_urteil, soll_clippen
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modki.py               frage, lies_klassifikation, lies_schimpfwoerter
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
outcomes.py            get_outcome_breakdown
overlaytext.py         configure, latest_popularity, ov_atomic_write, ov_bar, ov_oneline, overlay_src_ok
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
resolvergrund.py       http_grund, quelle_lage, quelle_laut, text
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, fenstergroesse, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, url_host
restreamcfg.py         active_platforms, aktiv, bereite_ziele, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamcmd.py         build, configure, drossel_avatar_aus, drossel_bitrate, drossel_canvas, drossel_fps, drossel_preset, drossel_zusatz, schriftart
restreamgesundheit.py  blind_markieren, frische_tee_fehler, marke_setzen
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              create_schema
schemastand.py         lege_an, lies, pruefe, schreibe, streng
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
telegramfehler.py      dauer_text, grund, ist_fehler, text, zuruecksetzen
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
tonspur.py             class Fehlschlag, hat_ton, hat_tonspur, ist_tonlos_fehler, nachruest_cmd, pruef_cmd, pruefen, sichern, stille_eingabe
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
tunnelwacht.py         lage, meldung, probe, probe_cmd
twitchoauth.py         access_token, authorize_url, configure, create_clip, exchange_code, forget, login_name, search_category, status, timeout_user, update_channel
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             build_stamp, changelog, current, latest, summary_line
videoteil.py           configure, dauer, ist_kaputter_container, kopier_teilen, neu_kodieren, platz_reicht, reparieren, wegwerfen, zeitstempel_richten, zu_gross
webserver.py           bindung, ist_loopback, schema, threads, tls_lage, waehle
whispercfg.py          geladen, name, verfuegbar, waehle
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytdlpurl.py            urls_aus_json
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status, upload_clip
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
